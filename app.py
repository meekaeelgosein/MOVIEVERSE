import os
import requests

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from genres import GENRE_MAP, get_genres_id # Import the GENRE_MAP from genres.py
from helpers import fetch_movies_from_api_all, fetch_movies_from_api_pop, get_streaming_services, get_movies  # Import helper functions

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY", "supersecretkey")

# Initialize the database
db = SQLAlchemy(app)

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    watchlist = db.relationship('WatchedMovie', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# WatchedMovie model
class WatchedMovie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/about')
def about():
    return render_template('about.html')
    
@app.route('/home')
def home():
    # logic for the home page
    return render_template("index.html")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes and view functions

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        genre = request.form.get("genre")
        release_date = request.form.get("year")  # Ensure 'year' is used in the form
        actor = request.form.get("actor")
        return redirect(url_for("results", genre=genre, release_date=release_date, actor=actor))
    
    # Fetch popular movies for display
    popular_movies = fetch_movies_from_api_pop()
    popular_movies = popular_movies[:18]  # Limit to the first 18 movie

    # Fetch genres
    genres = [genre["name"] for genre in GENRE_MAP["genres"]]

    return render_template("index.html", movies=popular_movies, genres=genres)

@app.route("/results", methods=["GET", "POST"])
@login_required
def results():
    primary_release_year = range(1900, 2025)  # Years for year filter
    genres = list(GENRE_MAP.keys()) # Fetch genres from GENRE_MAP keys

    # Initialize filters
    genre = ""
    year = ""
    actor = ""

    genres = [genre["name"] for genre in GENRE_MAP["genres"]]


    # Handle both POST and GET requests
    if request.method == "POST":
        genre = request.form.get("genre", "").strip()
        year = request.form.get("primary_release_date", "").strip()
        actor = request.form.get("actor", "").strip()
    else:  # GET request
        genre = request.args.get("genre", "").strip()
        year = request.args.get("primary_release_date", "").strip()
        actor = request.args.get("actor", "").strip()

    # Debugging: Print active filters
    print(f"Filters - Genre: {genre}, Year: {year}, Actor: {actor}")

    # Fetch movies based on the filters
    movies_data = fetch_movies_from_api_all(
        query=None, genre=genre, year=year, actor=actor
    )

    # Add streaming services for each movie
    for movie in movies_data:
        movie_id = movie["id"]
        movie["streaming_services"] = get_streaming_services(movie_id)

    # Render results template with genres and year range
    return render_template(
        "results.html",
        movies=movies_data,
        genres=genres,
        primary_release_year=primary_release_year,
        selected_genre=genre,
        selected_year=year,
        selected_actor=actor
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Username already exists. Please choose a different one.")
            return redirect(url_for("register"))
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        flash("Registration successful. You are now logged in.")
        return redirect(url_for("index"))
    
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful.")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("index"))

@app.route("/watchlist")
@login_required
def watchlist():
    user_movies = WatchedMovie.query.filter_by(user_id=current_user.id).all()
    return render_template("watchlist.html", user_movies=user_movies)

@app.route("/add_to_watchlist/<int:movie_id>/<string:title>")
@login_required
def add_to_watchlist(movie_id, title):
    existing_movie = WatchedMovie.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if existing_movie:
        flash("This movie is already in your watchlist.")
    else:
        movie = WatchedMovie(movie_id=movie_id, title=title, user_id=current_user.id)
        db.session.add(movie)
        db.session.commit()
        flash("Movie added to your watchlist.")
    return redirect(url_for("watchlist"))

# Code to view database contents and should be removed after application is determined to be fully functional
@app.route("/view_db")
def view_db():
    users = User.query.all()
    watched_movies = WatchedMovie.query.all()
    
    user_data = [{"id": user.id, "username": user.username} for user in users]
    movie_data = [{"id": movie.id, "movie_id": movie.movie_id, "title": movie.title, "user_id": movie.user_id} for movie in watched_movies]
    
    return render_template("view_db.html", users=user_data, watched_movies=movie_data)

# Run the app
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change the port to 5001 or any other available port








