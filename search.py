# search.py
import pandas as pd
from recommend import find_similar_titles, get_title_suggestions
def get_movie_data(movie_id, movies_df):
    return movies_df[movies_df["movieId"] == movie_id].reset_index(drop=True)

def search_movie_by_title(query, movies_df, top_n=10,fuzzy = True):
    # Exact search first
    exact_matches = movies_df[movies_df['title'].str.contains(query, case=False, na=False)]
    
    if not exact_matches.empty:
        return exact_matches.head(top_n)
    
    # Fuzzy search if no exact matches
    if fuzzy:
        suggestions = get_title_suggestions(query, movies_df, n=top_n)
        if suggestions:
            fuzzy_matches = movies_df[movies_df['title'].isin(suggestions)]
            return fuzzy_matches.head(top_n)
    
    return pd.DataFrame()  # Empty DataFrame if no matches
