import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql.functions import explode


# טעינת קובץ CSV עם Pandas
user_reviews_subset = pd.read_csv("movieReview/encoded_user_reviews_subset_01.csv")

# # קידוד movieId ו-userId לערכים שלמים
# user_reviews_subset['movieId_encoded'] = user_reviews_subset['movieId'].astype('category').cat.codes
# user_reviews_subset['userId_encoded'] = user_reviews_subset['userId'].astype('category').cat.codes
#
#
# # שמירת הנתונים המקודדים כקובץ CSV חדש
# user_reviews_subset.to_csv("movieReview/encoded_user_reviews_subset_helf.csv", index=False)

# יצירת SparkSession עם הגדרות זיכרון מוגדלות ומספר מעבדים מוגדל
spark = SparkSession.builder \
    .appName("ALS Recommendations with Hyperparameter Tuning") \
    .config("spark.driver.memory", "16g") \
    .config("spark.executor.memory", "16g") \
    .config("spark.executor.cores", "4") \
    .config("spark.sql.shuffle.partitions", "300") \
    .config("spark.default.parallelism", "300") \
    .config("spark.driver.maxResultSize", "4g") \
    .getOrCreate()

# טעינת הנתונים המקודדים כ-Spark DataFrame
user_reviews_spark_df = spark.createDataFrame(user_reviews_subset)
# user_reviews_spark_df = user_reviews_spark_df.sample(fraction=0.5)

# הגדלת מספר ה-Partitions
# user_reviews_spark_df = user_reviews_spark_df.repartition(500)

# שימוש ב-Caching
user_reviews_spark_df.cache()

# # המרת movieId_encoded ו-userId_encoded לנתונים מספריים
# user_reviews_spark_df = user_reviews_spark_df.withColumn("movieId_encoded", user_reviews_spark_df["movieId_encoded"])
# user_reviews_spark_df = user_reviews_spark_df.withColumn("userId_encoded", user_reviews_spark_df["userId_encoded"])

# הגדרת מודל ALS
als = ALS(userCol="userId_encoded", itemCol="movieId_encoded", ratingCol="rating", coldStartStrategy="drop")

# הגדרת הרשת של הפרמטרים
paramGrid = ParamGridBuilder() \
    .addGrid(als.rank, [20, 30]) \
    .addGrid(als.maxIter, [20]) \
    .addGrid(als.regParam, [0.1]) \
    .build()


# הגדרת הערכת המודל
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

# הגדרת קרוס-וולידציה
cv = CrossValidator(estimator=als, estimatorParamMaps=paramGrid, evaluator=evaluator, numFolds=5)

# חלוקת הנתונים לנתוני אימון ונתוני בדיקה
(training, test) = user_reviews_spark_df.randomSplit([0.8, 0.2])

# אימון המודל עם קרוס-וולידציה
cv_model = cv.fit(training)

# ביצוע תחזיות על נתוני הבדיקה
predictions = cv_model.transform(test)

# הערכת המודל באמצעות RMSE
rmse = evaluator.evaluate(predictions)
print(f"Root-mean-square error = {rmse}")

# הצגת הפרמטרים הטובים ביותר
best_model = cv_model.bestModel
print(f"Best rank: {best_model.rank}")
print(f"Best maxIter: {best_model._java_obj.parent().getMaxIter()}")
print(f"Best regParam: {best_model._java_obj.parent().getRegParam()}")

#cv_model.save("model")
#
# user_recommendations = best_model.recommendForAllUsers(10)
# movie_recommendations = best_model.recommendForAllItems(10)
#
#
# # Flatten user recommendations
# user_recs_exploded = user_recommendations.withColumn("recommendation", explode("recommendations")) \
#     .select("userId_encoded", "recommendation.movieId_encoded", "recommendation.rating")
#
# # Flatten movie recommendations
# movie_recs_exploded = movie_recommendations.withColumn("recommendation", explode("recommendations")) \
#     .select("movieId_encoded", "recommendation.userId_encoded", "recommendation.rating")
#
# # Save flattened user recommendations
# user_recs_exploded.write.csv("user_recommendations.csv", header=True, mode="overwrite")
#
# # Save flattened movie recommendations
# movie_recs_exploded.write.csv("movie_recommendations.csv", header=True, mode="overwrite")


spark.stop()