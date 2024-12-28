import os
import requests
from dotenv import load_dotenv
from genres import GENRE_MAP, get_genres_id

# Load environment variables from .env file
load_dotenv()

# Fetch the TMDB API key from environment variables
api_key = os.getenv('API_KEY')
print("API Key:", api_key)

# Your TMDB base URL
TMDB_BASE_URL = "https://api.themoviedb.org/3/"

def fetch_movies_from_api_pop():
    url = f"{TMDB_BASE_URL}movie/popular?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        return []

def fetch_movies_from_api_all(query=None, genre=None, year=None, actor=None):
    params = {
        "api_key": api_key,
        "language": "en-US",
        "sort_by": "popularity.desc",
        "page": 1,
        "append_to_response": "overview"
    }

    if query:
        params["query"] = query
        url = f"{TMDB_BASE_URL}search/movie"
    else:
        url = f"{TMDB_BASE_URL}discover/movie"

    if genre:
        genre_id = get_genres_id(genre)
        if genre_id:
            params["with_genres"] = genre_id

    if year:
        params["primary_release_year"] = year

    if actor:
        actor_id = get_actor_id(actor)
        if actor_id:
            params["with_cast"] = actor_id

    print(f"API params: {params}")  # Debugging

    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_actor_id(actor_name):
    api_url = f"{TMDB_BASE_URL}search/person"
    params = {
        "api_key": api_key,
        "language": "en-US",
        "query": actor_name,
        "page": 1,
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        results = response.json().get("results", [])
        if results:
            return results[0].get("id")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching actor ID: {e}")
    return None

def get_streaming_services(movie_id):
    url = f"{TMDB_BASE_URL}movie/{movie_id}/watch/providers?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json().get('results', {})
    else:
        return {}

def get_movies(genre=None, year=None, actor=None):
    movies = fetch_movies_from_api_all(genre=genre, year=year, actor=actor)
    if not movies:
        print(f"Final Year value being sent to fetch_movies_from_api_all: {year}")
        print("No movies fetched from the API.")
    return movies

