import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql import Row

# טעינת קובץ CSV עם Pandas
user_reviews_subset = pd.read_csv("movieReview/cleaned_user_reviews_subset.csv")

user_reviews_subset['movieId_encoded'] = user_reviews_subset['movieId'].astype('category').cat.codes
user_reviews_subset['userId_encoded'] = user_reviews_subset['userId'].astype('category').cat.codes
# הצגת דוגמאות מהנתונים
print(user_reviews_subset.head())

# יצירת SparkSession
spark = SparkSession.builder \
    .appName("ALS Recommendations") \
    .config("spark.driver.memory", "16g") \
    .config("spark.executor.memory", "16g") \
    .getOrCreate()

# המרת נתוני Pandas ל-Spark DataFrame
user_reviews_spark_df = spark.createDataFrame(user_reviews_subset)

# הצגת דוגמאות מהנתונים
user_reviews_spark_df.show(5)


als = ALS(maxIter=10, regParam=0.01, userCol="userId_encoded", itemCol="movieId_encoded", ratingCol="rating", coldStartStrategy="drop")

# חלוקת הנתונים לנתוני אימון ונתוני בדיקה
(training, test) = user_reviews_spark_df.randomSplit([0.8, 0.2])

# אימון המודל
model = als.fit(training)

# ביצוע תחזיות על נתוני הבדיקה
predictions = model.transform(test)

# הערכת המודל באמצעות RMSE
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")

# הצגת תחזיות
predictions.show(5)

# יצירת המלצות לכל משתמש
userRecs = model.recommendForAllUsers(10)

# הצגת המלצות לדוגמה
userRecs.show(5)

# יצירת המלצות לכל פריט (סרט)
movieRecs = model.recommendForAllItems(10)

# הצגת המלצות לדוגמה
movieRecs.show(5)

spark.stop()