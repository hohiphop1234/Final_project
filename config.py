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

# Recommendation constants
DEFAULT_MIN_RATING = 3.0
DEFAULT_MIN_RATING_COUNT = 5
DEFAULT_TOP_N = 10

# Fuzzy search constants
FUZZY_MIN_SCORE = 50
FUZZY_CONFIDENCE_THRESHOLD = 60

# Scoring weights
GENRE_WEIGHT = 0.4
RATING_WEIGHT = 0.6

# Hybrid recommendation weights
SIMILARITY_WEIGHT = 0.5
RATING_SCORE_WEIGHT = 0.3
PREFERENCE_WEIGHT = 0.2

# Performance settings
TFIDF_MAX_FEATURES = 1000
