# data_loader.py
import os
import pandas as pd
from config import MOVIES_PATH, RATINGS_PATH, USERS_PATH, MOVIE_COLS, GENRE_COLS
from utils import extract_year, row_genres, normalize_title

def load_data():
    movies = pd.read_csv(MOVIES_PATH, sep="|", encoding="latin-1", header=None, names=MOVIE_COLS)
    ratings = pd.read_csv(RATINGS_PATH, sep="\t", names=["userId","movieId","rating","timestamp"])
    users = pd.read_csv(USERS_PATH, sep="|", header=None, names=["userId","age","gender","occupation","zip_code"])
    
    # Drop unneeded cols
    movies = movies.drop(["video_release_date", "IMDb_URL"], axis=1)
    ratings = ratings.drop(["timestamp"], axis=1)
    users = users.drop(["zip_code"], axis=1)
    
    # Process movies
    movies["genres"] = movies.apply(lambda row: row_genres(row, GENRE_COLS), axis=1)
    movies["year"] = movies["title"].apply(extract_year)
    movies["title"] = movies["title"].str.replace(r"\s*\(\d{4}\)\s*$", "", regex=True)
    movies["title"] = movies["title"].apply(normalize_title)  
    movies_df = movies[["movieId","title","genres","year"]]
    
    return movies_df, ratings, users

def save_processed(movies_df, ratings, users, out_dir="processed"):
    os.makedirs(out_dir, exist_ok=True)
    movies_csv = os.path.join(out_dir, "movies_preprocessed.csv")
    ratings_csv = os.path.join(out_dir, "ratings.csv")
    users_csv = os.path.join(out_dir, "users.csv")
    
    movies_df.to_csv(movies_csv, index=False, encoding="utf-8")
    ratings.to_csv(ratings_csv, index=False)
    users.to_csv(users_csv, index=False)
    
    return movies_csv, ratings_csv, users_csv
