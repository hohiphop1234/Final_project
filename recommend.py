# recommend.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import (
    DEFAULT_MIN_RATING, DEFAULT_MIN_RATING_COUNT, DEFAULT_TOP_N,
    GENRE_WEIGHT, RATING_WEIGHT, SIMILARITY_WEIGHT, 
    RATING_SCORE_WEIGHT, PREFERENCE_WEIGHT, TFIDF_MAX_FEATURES
)
from search import fuzzy_search_movie_by_title

def build_similarity_matrix(movies_df):
    """Xây dựng ma trận cosine similarity dựa trên genres"""
    if movies_df.empty or 'genres' not in movies_df.columns:
        return None, None
    
    # Fill missing genres và build TF-IDF matrix
    genres_filled = movies_df['genres'].fillna('unknown')
    tfidf = TfidfVectorizer(stop_words='english', max_features=TFIDF_MAX_FEATURES)
    tfidf_matrix = tfidf.fit_transform(genres_filled)
    
    # Compute cosine similarity và create indices
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(movies_df.index, index=movies_df['title'].fillna('unknown')).drop_duplicates()
    
    return cosine_sim, indices

def recommend(title, movies_df, cosine_sim, indices, top_n=10, return_scores=False):
    """Gợi ý phim tương tự dựa trên cosine similarity"""
    # Fallback search if title not found
    if title not in indices:
        similar = movies_df[movies_df['title'].str.contains(title, case=False, na=False)]
        if not similar.empty:
            # Try with first match
            best_match = similar.iloc[0]['title']
            if best_match in indices:
                return recommend(best_match, movies_df, cosine_sim, indices, top_n, return_scores)
            return similar[['title', 'genres', 'year', 'avg_rating', 'rating_count']].head(5)
        return pd.DataFrame()
    
    # Get similarity scores
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    # Create result
    movie_indices = [i[0] for i in sim_scores]
    result = movies_df.iloc[movie_indices][['title', 'genres', 'year', 'avg_rating', 'rating_count']].copy()
    
    if return_scores:
        result['similarity_score'] = [round(score[1], 3) for score in sim_scores]
    
    return result

def recommend_by_genres(movies_df, preferred_genres, top_n=DEFAULT_TOP_N, min_rating=DEFAULT_MIN_RATING, min_rating_count=DEFAULT_MIN_RATING_COUNT):
    """Gợi ý phim theo thể loại yêu thích với điểm rating"""
    if isinstance(preferred_genres, str):
        preferred_genres = [preferred_genres]
    
    if not preferred_genres or movies_df.empty:
        return pd.DataFrame()
    
    # Tính genre score
    movies_copy = movies_df.copy()
    movies_copy['genre_score'] = 0.0
    
    for genre in preferred_genres:
        if genre:
            mask = movies_copy['genres'].str.contains(genre, case=False, na=False)
            movies_copy.loc[mask, 'genre_score'] += 1.0
    
    # Filter movies
    result = movies_copy[
        (movies_copy['genre_score'] > 0) & 
        (movies_copy['avg_rating'] >= min_rating) & 
        (movies_copy['rating_count'] >= min_rating_count)
    ].copy()
    
    if result.empty:
        return pd.DataFrame()
    
    # Calculate final score
    max_genre_score = result['genre_score'].max()
    result['genre_score_norm'] = result['genre_score'] / max_genre_score if max_genre_score > 0 else 0
    result['final_score'] = (result['avg_rating'] / 5.0) * RATING_WEIGHT + result['genre_score_norm'] * GENRE_WEIGHT
    
    return result.sort_values(['final_score', 'rating_count'], ascending=[False, False]).head(top_n)[
        ['title', 'genres', 'year', 'avg_rating', 'rating_count', 'genre_score', 'final_score']
    ]

def get_genre_recommendations(movies_df, cosine_sim, indices, genres_list, top_n=5):
    """Gợi ý phim cho từng thể loại"""
    recommendations = {}
    
    for genre in genres_list:
        genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
        if not genre_movies.empty:
            seed_movie = genre_movies.iloc[0]['title']
            recommendations[genre] = recommend(seed_movie, movies_df, cosine_sim, indices, top_n)
    
    return recommendations

def hybrid_recommend(title, movies_df, cosine_sim, indices, user_preferences=None, top_n=DEFAULT_TOP_N):
    """Hybrid recommendation kết hợp content-based, user preferences và ratings với fuzzy search"""
    # Try exact match first, then fuzzy search
    if title not in indices:
        fuzzy_results = fuzzy_search_movie_by_title(title, movies_df)
        if not fuzzy_results.empty:
            title = fuzzy_results.iloc[0]['title']  # Use best fuzzy match
        else:
            return pd.DataFrame()  # No matches found
    
    # Get content-based recommendations
    content_recs = recommend(title, movies_df, cosine_sim, indices, top_n*2, return_scores=True)
    
    if content_recs.empty or not user_preferences:
        return content_recs.head(top_n)
    
    # Add user preference scoring (explicitly set as float to avoid dtype warning)
    content_recs['bonus_score'] = 0.0
    
    # Genre preferences
    for genre in user_preferences.get('genres', []):
        if genre:
            mask = content_recs['genres'].str.contains(genre, case=False, na=False)
            content_recs.loc[mask, 'bonus_score'] += 0.1
    
    # Year preferences
    year_range = user_preferences.get('year_range', None)
    if year_range and len(year_range) == 2:
        year_mask = (content_recs['year'].notna() & 
                    (content_recs['year'] >= year_range[0]) & 
                    (content_recs['year'] <= year_range[1]))
        content_recs.loc[year_mask, 'bonus_score'] += 0.05
    
    # Calculate final hybrid score
    content_recs['rating_score'] = content_recs['avg_rating'].fillna(3.0) / 5.0
    content_recs['final_score'] = (
        content_recs['similarity_score'].fillna(0) * SIMILARITY_WEIGHT + 
        content_recs['rating_score'] * RATING_SCORE_WEIGHT + 
        content_recs['bonus_score'] * PREFERENCE_WEIGHT
    )
    
    return content_recs.sort_values(['final_score', 'rating_count'], ascending=[False, False]).head(top_n)
