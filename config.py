# config.py
import os

# Paths
BASE_DIR = os.path.join('movielens-100k-dataset', 'ml-100k')
RATINGS_PATH = os.path.join(BASE_DIR, 'u.data')
MOVIES_PATH = os.path.join(BASE_DIR, 'u.item')
USERS_PATH = os.path.join(BASE_DIR, 'u.user')

# Columns
GENRE_COLS = [
    "unknown","Action","Adventure","Animation","Children's","Comedy","Crime","Documentary",
    "Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"
]
MOVIE_COLS = ["movieId","title","release_date","video_release_date","IMDb_URL"] + GENRE_COLS
