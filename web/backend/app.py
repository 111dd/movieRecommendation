from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# התחברות למונגו
client = MongoClient('mongodb://localhost:27017/')
db = client['movies']
collection = db['moviesReview']
users_collection = db['users']

# פונקציית עזר ליצירת משתמש חדש
def create_user(username, password):
    hashed_password = generate_password_hash(password)
    user = {
        "username": username,
        "password": hashed_password,
        "liked_movies": [],
        "recommended_movies": []
    }
    users_collection.insert_one(user)

# פונקציה לקבלת משתמש לפי שם משתמש
def get_user(username):
    return users_collection.find_one({"username": username})

# פונקציה לבדוק סיסמת משתמש
def check_user_password(username, password):
    user = get_user(username)
    if user and check_password_hash(user['password'], password):
        return True
    return False

# מסלול רישום
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = get_user(username)
        if existing_user is None:
            create_user(username, password)
            return redirect(url_for('login'))
        else:
            return 'User already exists!'
    return render_template('register.html')

# מסלול כניסה
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user_password(username, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return 'Invalid credentials!'
    return render_template('login.html')

# מסלול יציאה
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# מסלול דף הבית
@app.route('/')
def index():
    username = session.get('username')
    return render_template('index.html', username=username)

# מסלול כל הסרטים
@app.route('/movies')
def movies():
    username = session.get('username')
    return render_template('movies.html', username=username)

# מסלול סרט מסוים
@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    username = session.get('username')
    return render_template('movie_detail.html', movie_id=movie_id, username=username)

# מסלולי API לסרטים
@app.route('/api/movies', methods=['GET'])
def get_movies():
    recent_movies = list(collection.find().limit(20))
    sorted_movies = sorted(recent_movies, key=lambda x: x.get('critic_score', 0), reverse=True)
    top_movies = sorted_movies[:10]

    for movie in top_movies:
        movie['_id'] = str(movie['_id'])  # המרה ל-JSON serializable

    return jsonify(top_movies)

@app.route('/api/movies/all', methods=['GET'])
def get_all_movies():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))

    skip = (page - 1) * per_page
    all_movies = list(collection.find().skip(skip).limit(per_page))

    total_movies = collection.count_documents({})
    total_pages = (total_movies + per_page - 1) // per_page

    for movie in all_movies:
        movie['_id'] = str(movie['_id'])  # המרה ל-JSON serializable

    return jsonify({
        'movies': all_movies,
        'total_pages': total_pages,
        'current_page': page
    })

@app.route('/api/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = collection.find_one({'movieId': movie_id})
    if movie:
        movie['_id'] = str(movie['_id'])  # המרה ל-JSON serializable
        return jsonify(movie)
    return jsonify({'error': 'Movie not found'}), 404

@app.route('/api/search_movies', methods=['GET'])
def search_movies():
    query = request.args.get('q')
    movies = list(collection.find({'movieTitle': {'$regex': query, '$options': 'i'}}))
    for movie in movies:
        movie['_id'] = str(movie['_id'])
    return jsonify(movies)

@app.route('/api/movies/like', methods=['POST'])
def like_movie():
    user_id = request.json['user_id']
    movie_id = request.json['movie_id']
    users_collection.update_one({'username': user_id}, {'$addToSet': {'liked_movies': movie_id}})
    return jsonify(success=True)

# מסלול API לרישום
@app.route('/api/register', methods=['POST'])
def api_register():
    username = request.json['username']
    password = request.json['password']
    existing_user = get_user(username)
    if existing_user is None:
        create_user(username, password)
        return jsonify({'message': 'User registered successfully'})
    else:
        return jsonify({'error': 'User already exists!'}), 400

# מסלול API לכניסה
@app.route('/api/login', methods=['POST'])
def api_login():
    username = request.json['username']
    password = request.json['password']
    if check_user_password(username, password):
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid credentials!'}), 401

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)