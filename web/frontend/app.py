from flask import Flask, render_template, request, redirect, url_for, session
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'

api_base_url = 'http://localhost:5000/api'

@app.route('/')
def index():
    if 'user_id' in session:
        response = requests.get(f'{api_base_url}/movies')
        movies = response.json() if response.status_code == 200 else []
        return render_template('index.html', movies=movies)
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{api_base_url}/login', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user_id'] = username
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        response = requests.post(f'{api_base_url}/register', json={'username': username, 'password': password})
        if response.status_code == 200:
            session['user_id'] = username
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/movies', methods=['GET'])
def movies():
    return render_template('movies.html')

@app.route('/movie/<movie_id>')
def movie_detail(movie_id):
    return render_template('movie_detail.html', movie_id=movie_id)

if __name__ == '__main__':
    app.run(debug=True, port=5001)