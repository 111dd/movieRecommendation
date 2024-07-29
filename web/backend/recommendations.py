from pyspark.ml.recommendation import ALSModel
from pyspark.sql import SparkSession


class Recommendations:
    def __init__(self, db):
        self.db = db
        self.spark = SparkSession.builder.appName('Movies').getOrCreate()
        self.model = ALSModel.load('path_to_your_trained_model')

    def get_top_movies(self, user_id):
        user_recs = self.model.recommendForUserSubset(self.spark.createDataFrame([(user_id,)], ["userId"]), 10)
        movie_ids = [row.movieId for row in user_recs.collect()]
        movies = list(self.db.get_movies_collection().find({'movieId': {'$in': movie_ids}}))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies

    def get_all_movies(self, page, per_page):
        skip = (page - 1) * per_page
        movies = list(self.db.get_movies_collection().find().skip(skip).limit(per_page))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        total_movies = self.db.get_movies_collection().count_documents({})
        return {'movies': movies, 'total_pages': (total_movies + per_page - 1) // per_page, 'current_page': page}

    def get_movie_details(self, movie_id):
        movie = self.db.get_movies_collection().find_one({'movieId': movie_id})
        if movie:
            movie['_id'] = str(movie['_id'])
        return movie

    def search_movies(self, query):
        movies = list(self.db.get_movies_collection().find({'movieTitle': {'$regex': query, '$options': 'i'}}))
        for movie in movies:
            movie['_id'] = str(movie['_id'])
        return movies

    def like_movie(self, user_id, movie_id):
        self.db.get_users_collection().update_one({'username': user_id}, {'$addToSet': {'liked_movies': movie_id}})
        # Optionally update recommendations