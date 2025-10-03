# recommend.py
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from difflib import get_close_matches
import re
def build_similarity_matrix(movies_df):
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies_df['genres'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(movies_df.index, index=movies_df['title']).drop_duplicates()
    return cosine_sim, indices, tfidf_matrix, tfidf
def find_similar_titles(input_title, all_titles, n=5, cutoff=0.3):
    close_matches = get_close_matches(input_title, all_titles, n = n, cutoff= cutoff)
    if not close_matches:
        keywords = re.findall(r'\w+', input_title.lower())
        for title in all_titles:
            title_lower = title.lower()
            if any(keyword in title_lower for keyword in keywords if len(keyword)>2):
                close_matches.append(title)
                if len(close_matches) >= n:
                    break
    return close_matches
def recommend(title, movies_df, cosine_sim, indices, top_n=10):
    all_titles = movies_df['title'].tolist()
    
    if title in indices:
        exact_title = title
    else:
        similar_titles = find_similar_titles(title, all_titles)
        if not similar_titles:
            return pd.DataFrame()  # ← Trả về DataFrame rỗng thay vì string
        
        exact_title = similar_titles[0]  # Dùng kết quả đầu tiên, bỏ suggestion logic
    
    # Thực hiện recommendation
    idx = indices[exact_title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [(i, score) for i, score in sim_scores if i != idx]
    sim_scores = sim_scores[:top_n]
    movie_indices = [i[0] for i in sim_scores]
    
    result = movies_df.iloc[movie_indices][['title','genres']].copy()
    result['similarity_score'] = [score for _, score in sim_scores]
    
    return result

def get_title_suggestions(partial_title, movies_df, n=5):
    #Kieu nhu auto complete
    all_titles = movies_df['title'].tolist()
    return find_similar_titles(partial_title,all_titles, n=n, cutoff=0.2)
    