# data_loader.py
import os
import pandas as pd
from config import MOVIES_PATH, RATINGS_PATH, USERS_PATH, MOVIE_COLS, GENRE_COLS
from utils import extract_year, row_genres

def calculate_movie_ratings(ratings):
    """Tính điểm trung bình và số lượng rating cho mỗi phim"""
    try:
        if ratings.empty:
            return pd.DataFrame(columns=['movieId', 'avg_rating', 'rating_count'])
        
        movie_stats = ratings.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).round(2)
        
        # Flatten column names
        movie_stats.columns = ['avg_rating', 'rating_count']
        movie_stats = movie_stats.reset_index()
        
        return movie_stats
    except Exception as e:
        print(f"Warning: Error calculating movie ratings: {e}")
        # Return empty DataFrame with correct columns
        return pd.DataFrame(columns=['movieId', 'avg_rating', 'rating_count'])

def load_data():
    try:
        movies = pd.read_csv(MOVIES_PATH, sep="|", encoding="latin-1", header=None, names=MOVIE_COLS)
        ratings = pd.read_csv(RATINGS_PATH, sep="\t", names=["userId","movieId","rating","timestamp"])
        users = pd.read_csv(USERS_PATH, sep="|", header=None, names=["userId","age","gender","occupation","zip_code"])
        
        # Drop unneeded cols
        movies = movies.drop(["video_release_date", "IMDb_URL"], axis=1)
        ratings = ratings.drop(["timestamp"], axis=1)
        users = users.drop(["zip_code", "occupation"], axis=1)
        
        # Process movies
        movies["genres"] = movies.apply(lambda row: row_genres(row, GENRE_COLS), axis=1)
        movies["year"] = movies["title"].apply(extract_year)
        movies["title"] = movies["title"].str.replace(r"\s*\(\d{4}\)\s*$", "", regex=True)
        movies_df = movies[["movieId","title","genres","year"]]
        
        # Calculate and merge movie ratings
        movie_stats = calculate_movie_ratings(ratings)
        
        if not movie_stats.empty:
            movies_df = movies_df.merge(movie_stats, on='movieId', how='left')
        else:
            # Add empty columns if rating calculation failed
            movies_df['avg_rating'] = 3.0
            movies_df['rating_count'] = 0
        
        # Fill missing ratings with default values
        movies_df['avg_rating'] = movies_df['avg_rating'].fillna(3.0)
        movies_df['rating_count'] = movies_df['rating_count'].fillna(0)
        
        return movies_df, ratings, users
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Data files not found: {e}")
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def save_processed(movies_df, ratings, users, out_dir="processed"):
    os.makedirs(out_dir, exist_ok=True)
    movies_csv = os.path.join(out_dir, "movies_preprocessed.csv")
    ratings_csv = os.path.join(out_dir, "ratings.csv")
    users_csv = os.path.join(out_dir, "users.csv")
    
    movies_df.to_csv(movies_csv, index=False, encoding="utf-8")
    ratings.to_csv(ratings_csv, index=False)
    users.to_csv(users_csv, index=False)
    
    return movies_csv, ratings_csv, users_csv

# Run this function to loading and saving data
def main():
    print("Loading data...")
    movies_df, ratings, users = load_data()
    print(f"Movies loaded: {len(movies_df)}")
    print(f"Ratings loaded: {len(ratings)}")
    print(f"Users loaded: {len(users)}")
    
    print("Saving processed data...")
    movies_csv, ratings_csv, users_csv = save_processed(movies_df, ratings, users)
    print(f"Saved movies to: {movies_csv}")
    print(f"Saved ratings to: {ratings_csv}")
    print(f"Saved users to: {users_csv}")

if __name__ == "__main__":
    main()