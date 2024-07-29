from pyspark import SparkConf
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace

import pandas as pd

# טעינת קובץ CSV
file_path = "movieReview/encoded_user_reviews_subset.csv"
df = pd.read_csv(file_path)

# הצגת מספר השורות המקורי
print(f"Number of rows before sampling: {len(df)}")

# דגימה רנדומלית של מחצית מהשורות
df_sampled = df.sample(frac=0.1, random_state=42)

# הצגת מספר השורות לאחר הדגימה
print(f"Number of rows after sampling: {len(df_sampled)}")

# שמירת הנתונים החדשים כקובץ CSV חדש
output_file_path = "movieReview/encoded_user_reviews_subset_01.csv"
df_sampled.to_csv(output_file_path, index=False)

print(f"Sampled data saved to: {output_file_path}")