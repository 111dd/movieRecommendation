import pandas as pd

# טעינת קבצי CSV עם Pandas
# user_reviews_df = pd.read_csv("movieReview/cleaned_user_reviews.csv")
# print(user_reviews_df.isna().sum())
#
# user_reviews_cleaned = user_reviews_df.dropna()
#
# print(user_reviews_cleaned.isna().sum())
#
# user_reviews_cleaned.to_csv("movieReview/dropna_user_reviews.csv", index=False)

# user_reviews_df = pd.read_csv("movieReview/dropna_user_reviews.csv")


# columns_to_keep = ['movieId', 'rating', 'userId']
# user_reviews_subset = user_reviews_df[columns_to_keep]
#
# # הצגת דוגמאות מהנתונים עם העמודות הרצויות
# print(user_reviews_subset.head())
#
# # שמירת הנתונים עם העמודות הרצויות כקובץ CSV חדש
# user_reviews_subset.to_csv("movieReview/user_reviews_subset.csv", index=False)

user_reviews_df = pd.read_csv("movieReview/user_reviews_subset.csv")

def is_numeric(s):
    return s.isdigit()

# סינון השורות שבהן userId הוא מספרי בלבד
user_reviews_cleaned = user_reviews_df[user_reviews_df['userId'].apply(is_numeric)]

user_reviews_cleaned.to_csv("movieReview/cleaned_user_reviews_subset.csv", index=False)