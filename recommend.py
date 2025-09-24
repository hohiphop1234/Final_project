# recommend.py
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity_matrix(movies_df):
    """Xây dựng ma trận cosine similarity dựa trên genres"""
    # Cải tiến TfidfVectorizer cho hiệu quả tốt hơn
    tfidf = TfidfVectorizer(
        stop_words='english',
        max_features=1000,
        ngram_range=(1, 2),  # Sử dụng unigram và bigram
        min_df=1,
        max_df=0.8
    )
    
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()
    
    return cosine_sim, indices

def recommend(title, movies_df, cosine_sim, indices, top_n=10, return_scores=False):
    """
    Gợi ý phim tương tự dựa trên cosine similarity
    
    Args:
        title: Tên phim
        movies_df: DataFrame chứa thông tin phim
        cosine_sim: Ma trận similarity
        indices: Mapping title -> index
        top_n: Số lượng gợi ý
        return_scores: Có trả về similarity scores không
    """
    if title not in indices:
        # Tìm phim tương tự nếu không match exact
        similar = movies_df[movies_df['title'].str.contains(title, case=False, na=False)]
        if not similar.empty:
            return similar[['title', 'genres', 'year']].head(5)
        return pd.DataFrame()
    
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    movie_indices = [i[0] for i in sim_scores]
    result = movies_df.iloc[movie_indices][['title', 'genres', 'year']].copy()
    
    if return_scores:
        result['similarity_score'] = [round(score[1], 3) for score in sim_scores]
    
    return result

def recommend_by_genres(movies_df, preferred_genres, top_n=10):
    """Gợi ý phim theo thể loại yêu thích"""
    if isinstance(preferred_genres, str):
        preferred_genres = [preferred_genres]
    
    # Tính điểm dựa trên số thể loại khớp
    movies_df['genre_score'] = 0
    for genre in preferred_genres:
        movies_df.loc[movies_df['genres'].str.contains(genre, case=False, na=False), 'genre_score'] += 1
    
    # Lọc phim có ít nhất 1 thể loại khớp
    result = movies_df[movies_df['genre_score'] > 0].copy()
    result = result.sort_values('genre_score', ascending=False).head(top_n)
    
    return result[['title', 'genres', 'year', 'genre_score']]

def get_genre_recommendations(movies_df, cosine_sim, indices, genres_list, top_n=5):
    """Gợi ý phim cho từng thể loại"""
    recommendations = {}
    
    for genre in genres_list:
        # Tìm phim phổ biến nhất của thể loại này
        genre_movies = movies_df[movies_df['genres'].str.contains(genre, case=False, na=False)]
        if not genre_movies.empty:
            # Lấy phim đầu tiên làm seed
            seed_movie = genre_movies.iloc[0]['title']
            recs = recommend(seed_movie, movies_df, cosine_sim, indices, top_n)
            recommendations[genre] = recs
    
    return recommendations

def hybrid_recommend(title, movies_df, cosine_sim, indices, user_preferences=None, top_n=10):
    """
    Hybrid recommendation kết hợp content-based và user preferences
    """
    # Content-based recommendations
    content_recs = recommend(title, movies_df, cosine_sim, indices, top_n*2, return_scores=True)
    
    if user_preferences and not content_recs.empty:
        # Boost score dựa trên preferences của user
        preferred_genres = user_preferences.get('genres', [])
        preferred_years = user_preferences.get('year_range', None)
        
        # Tính bonus score
        content_recs['bonus_score'] = 0
        
        for genre in preferred_genres:
            mask = content_recs['genres'].str.contains(genre, case=False, na=False)
            content_recs.loc[mask, 'bonus_score'] += 0.1
        
        if preferred_years:
            year_mask = (content_recs['year'] >= preferred_years[0]) & (content_recs['year'] <= preferred_years[1])
            content_recs.loc[year_mask, 'bonus_score'] += 0.05
        
        # Tính final score
        content_recs['final_score'] = content_recs['similarity_score'] + content_recs['bonus_score']
        content_recs = content_recs.sort_values('final_score', ascending=False)
    
    return content_recs.head(top_n)
