from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['movies']

    def get_movies_collection(self):
        return self.db['moviesReview']

    def get_users_collection(self):
        return self.db['users']

    def insert_user(self, user):
        users_collection = self.get_users_collection()
        users_collection.insert_one(user)

    def find_user(self, username):
        users_collection = self.get_users_collection()
        return users_collection.find_one({'username': username})