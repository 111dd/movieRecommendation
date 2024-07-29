from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace

spark = SparkSession.builder \
    .appName("Load Parquet and Manipulate Data") \
    .getOrCreate()

# טעינת נתוני Parquet שנשמרו
user_reviews_df = spark.read.parquet("movieReview/user_reviews.parquet")
movies_df = spark.read.parquet("movieReview/movies.parquet")
critic_reviews_df = spark.read.parquet("movieReview/critic_reviews.parquet")


initial_count = user_reviews_df.count()
print(f"Initial count of rows: {initial_count}")


user_reviews_cleaned = user_reviews_df.dropna(subset=["movieId", "rating", "quote", "reviewId", "isVerified", "isSuperReviewer",\
                                                      "hasSpoilers", "hasProfanity", "score", "creationDate", "userDisplayName", "userRealm", "userId"])
initial_count = user_reviews_cleaned.count()
print(f"Initial count of rows: {initial_count}")
# הצגת דוגמאות מהנתונים
user_reviews_cleaned.show(5)

