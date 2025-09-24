# search.py
def get_movie_data(movie_id, movies_df):
    return movies_df[movies_df["movieId"] == movie_id].reset_index(drop=True)

def search_movie_by_title(q, movies_df, top_n=10):
    q_norm = q.strip().lower()
    m = movies_df[movies_df["title"].str.lower().str.contains(q_norm, na=False)]
    return m.head(top_n).reset_index(drop=True)
