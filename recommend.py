# recommend.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_similarity_matrix(movies_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()
    return cosine_sim, indices

def recommend(title, movies_df, cosine_sim, indices, top_n=10):
    if title not in indices:
        return f"Phim '{title}' không có trong dataset."
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Loại bỏ chính phim được tìm kiếm (theo index, không phải vị trí đầu tiên)
    sim_scores = [(i, score) for i, score in sim_scores if i != idx]
    
    # Lấy top_n phim tương tự nhất
    sim_scores = sim_scores[:top_n]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df.iloc[movie_indices][['title','genres']]
