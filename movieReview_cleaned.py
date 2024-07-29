import pandas as pd

# טעינת קבצי CSV עם Pandas
user_reviews_df = pd.read_csv("movieReview/user_reviews.csv/user_reviews.csv")


# הצגת דוגמאות מהנתונים
print(user_reviews_df.head())


# הסרת עמודות לא רצויות
columns_to_drop = ["creationDate", "userDisplayName", "userRealm", "reviewId",
                   "isVerified", "isSuperReviewer", "score", "hasSpoilers", "hasProfanity"]
user_reviews_cleaned = user_reviews_df.drop(columns=columns_to_drop)

print(user_reviews_cleaned.head())

user_reviews_cleaned.to_csv("movieReview/cleaned_user_reviews.csv", index=False)