from pymongo import MongoClient


def test_mongo_connection():
    try:
        # התחברות ל-MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['movies']
        collection = db['moviesReview']

        # בדיקת החיבור באמצעות שאילתת דוגמה
        sample_movie = collection.find_one()
        if sample_movie:
            print("Connection successful! Sample movie found:")
            print(sample_movie)
        else:
            print("Connection successful, but no movies found.")
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")


if __name__ == "__main__":
    test_mongo_connection()