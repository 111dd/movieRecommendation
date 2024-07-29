from flask import Flask, request, jsonify
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)

client = MongoClient('mongodb://localhost:27017/')
db = client['movies']
users_collection = db['users']

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json['username']
    password = request.json['password']
    if users_collection.find_one({'username': username}):
        return jsonify({'error': 'Username already exists'}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_collection.insert_one({'username': username, 'password': hashed_password})
    return jsonify({'message': 'User registered successfully'})

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    user = users_collection.find_one({'username': username})
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        return jsonify({'message': 'Login successful'})
    return jsonify({'error': 'Invalid username or password'}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5003)