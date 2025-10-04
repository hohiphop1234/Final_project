# search.py
try:
    from fuzzywuzzy import fuzz, process
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    print("Warning: fuzzywuzzy not installed. Using basic string matching.")

import pandas as pd
from config import FUZZY_MIN_SCORE, FUZZY_CONFIDENCE_THRESHOLD, DEFAULT_TOP_N

def preprocess_title(title):
    """Tiền xử lý title để so sánh tốt hơn"""
    if pd.isna(title) or not title:
        return ""
    
    # Chuyển về lowercase và loại bỏ khoảng trắng thừa
    title = str(title).lower().strip()
    
    # Loại bỏ "the", "a", "an" ở đầu
    prefixes = ["the ", "a ", "an "]
    for prefix in prefixes:
        if title.startswith(prefix):
            title = title[len(prefix):]
            break
    
    return title

def get_movie_data(movie_id, movies_df):
    """Get movie data by movie ID"""
    return movies_df[movies_df["movieId"] == movie_id].reset_index(drop=True)

def fuzzy_search_movie_by_title(q, movies_df, top_n=DEFAULT_TOP_N, min_score=FUZZY_CONFIDENCE_THRESHOLD):
    """
    Tìm kiếm phim sử dụng fuzzy matching với fuzzywuzzy
    
    Args:
        q: Query string
        movies_df: DataFrame chứa phim
        top_n: Số lượng kết quả trả về
        min_score: Điểm tối thiểu để coi là match (0-100)
    
    Returns:
        DataFrame với các phim match và confidence score
    """
    if not FUZZYWUZZY_AVAILABLE:
        # Fallback về exact search đơn giản
        q_norm = q.strip().lower()
        exact_matches = movies_df[movies_df["title"].str.lower().str.contains(q_norm, na=False)]
        result = exact_matches.head(top_n).reset_index(drop=True)
        if not result.empty:
            result['confidence_score'] = 100
        return result
    
    if not q.strip():
        return pd.DataFrame()
    
    # Preprocess query
    query_processed = preprocess_title(q)
    
    # Tạo dictionary mapping title -> index để dễ lookup
    title_to_index = {}
    for idx, title in enumerate(movies_df['title'].fillna('')):
        processed_title = preprocess_title(title)
        if processed_title:  # Chỉ add non-empty titles
            title_to_index[processed_title] = idx
    
    # Sử dụng fuzzywuzzy để tìm matches
    processed_titles = list(title_to_index.keys())
    matches = process.extract(
        query_processed, 
        processed_titles, 
        scorer=fuzz.WRatio,
        limit=top_n * 2
    )
    
    # Filter và tạo kết quả
    result_indices = []
    confidence_scores = []
    
    for match_title, score in matches:
        if score >= min_score and match_title in title_to_index:
            idx = title_to_index[match_title]
            result_indices.append(idx)
            confidence_scores.append(score)
            
            if len(result_indices) >= top_n:
                break
    
    if not result_indices:
        return pd.DataFrame()
    
    # Tạo result DataFrame
    result_df = movies_df.iloc[result_indices].copy()
    result_df['confidence_score'] = confidence_scores
    
    return result_df.reset_index(drop=True)

def search_movie_by_title(q, movies_df, top_n=DEFAULT_TOP_N, use_fuzzy=True):
    """
    Tìm kiếm phim với hybrid approach: exact search + fuzzy search
    
    Args:
        q: Query string
        movies_df: DataFrame chứa phim
        top_n: Số lượng kết quả
        use_fuzzy: Có sử dụng fuzzy search không
    """
    if not q.strip():
        return pd.DataFrame()
    
    q_norm = q.strip().lower()
    
    # 1. Thử exact substring match trước
    exact_matches = movies_df[movies_df["title"].str.lower().str.contains(q_norm, na=False)]
    
    # Nếu có kết quả exact match
    if not exact_matches.empty:
        result = exact_matches.head(top_n).reset_index(drop=True)
        result['confidence_score'] = 100  # Perfect match
        return result
    
    # 2. Nếu không có exact match và use_fuzzy=True, dùng fuzzy search
    if use_fuzzy and FUZZYWUZZY_AVAILABLE:
        fuzzy_result = fuzzy_search_movie_by_title(q, movies_df, top_n, min_score=FUZZY_MIN_SCORE)
        if not fuzzy_result.empty:
            return fuzzy_result
    
    # 3. Nếu không có gì, return empty DataFrame
    return pd.DataFrame()