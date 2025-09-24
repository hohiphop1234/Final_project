# For Python 3.13 compatibility, we'll skip opendatasets and use the existing dataset
# The MovieLens dataset is already available in the movielens-100k-dataset folder
import os
print("Using existing MovieLens dataset from movielens-100k-dataset folder")
print("Dataset files are already available in the workspace")
import os   # Used to read the images path from the directory
import re

# Data handling
import pandas as pd # Used to read/create dataframes (csv) and process tabular data
import numpy as np  # preprocessing and numerical/mathematical operations

# Visualization
import matplotlib.pyplot as plt # Used for visualizing the images and plotting the training progress
import seaborn as sns

# Preprocessing & similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
# Use relative paths for the local dataset
base_dir = os.path.join('movielens-100k-dataset','ml-100k')
ratings_path = os.path.join(base_dir,'u.data')
movies_path = os.path.join(base_dir,'u.item')
users_path = os.path.join(base_dir,'u.user')

print(f"Base directory: {base_dir}")
print(f"Ratings file: {ratings_path}")
print(f"Movies file: {movies_path}")
print(f"Users file: {users_path}")
genre_cols = [
    "unknown","Action","Adventure","Animation","Children's","Comedy","Crime","Documentary",
    "Drama","Fantasy","Film-Noir","Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"
]
movie_cols = ["movieId","title","release_date","video_release_date","IMDb_URL"] + genre_cols

movies = pd.read_csv(movies_path, sep="|", encoding="latin-1", header=None, names=movie_cols)

ratings = pd.read_csv(ratings_path, sep="\t", names=["userId","movieId","rating","timestamp"])

users = pd.read_csv(users_path, sep="|", header=None, names=["userId","age","gender","occupation","zip_code"])

# Drop columns we don’t need
movies = movies.drop(["video_release_date", "IMDb_URL"], axis=1)

print("Prepared Ratings Shape:", ratings.shape)
print("Prepared Movies Shape:", movies.shape)
print(ratings.isnull().sum())
print(movies.isnull().sum())
def extract_year(title: str):
    if not isinstance(title, str):
        return np.nan
    m = re.search(r"\((\d{4})\)", title)
    return int(m.group(1)) if m else np.nan
def row_genres(row):
    g = [g for g in genre_cols if row[g] == 1]
    return "  ".join(g) if g else "unknown"

movies["genres"] = movies.apply(row_genres, axis=1)
movies["year"] = movies["title"].apply(extract_year)

# làm sạch title: bỏ "(1995)" nếu muốn
movies["title_clean"] = movies["title"].str.replace(r"\s*\(\d{4}\)\s*$", "", regex=True)

# DataFrame đầu ra
movies_df = movies[["movieId", "title_clean", "genres", "year"]].rename(columns={"title_clean": "title"})

# # Create processed directory in the current working directory
# out_dir = "processed"
# os.makedirs(out_dir, exist_ok=True)

# movies_csv = os.path.join(out_dir, "movies_preprocessed.csv")
# ratings_csv = os.path.join(out_dir, "ratings.csv")
# users_csv = os.path.join(out_dir, "users.csv")

# movies_df.to_csv(movies_csv, index=False, encoding="utf-8")
# ratings.to_csv(ratings_csv, index=False)
# users.to_csv(users_csv, index=False)
# print("Saved:", movies_csv)
# print("Saved:", ratings_csv)
# print("Saved:", users_csv)

#lấy dữ liệu phim theo id / tìm theo tên
def get_movie_data(movie_id: int):
    return movies_df[movies_df["movieId"] == movie_id].reset_index(drop=True)

def search_movie_by_title(q: str, top_n: int = 10):
    q_norm = q.strip().lower()
    m = movies_df[movies_df["title"].str.lower().str.contains(q_norm, na=False)]
    return m.head(top_n).reset_index(drop=True)
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Dùng TF-IDF để biến thể loại thành vector
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])



# Ma trận cosine similarity giữa các phim
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)


def recommend(title, top_n=10):
    # Mapping từ tên phim sang index
    indices = pd.Series(movies.index, index=movies['title_clean']).drop_duplicates()

    if title not in indices:
        return f"Phim '{title}' không có trong dataset."

    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]  # Bỏ chính nó
    movie_indices = [i[0] for i in sim_scores]

    return movies.iloc[movie_indices][['title_clean', 'genres']]
