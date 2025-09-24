import os
from typing import List, Tuple
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import numpy as np

from data_loader import load_data
from recommend import (
    build_similarity_matrix, recommend, recommend_by_genres, 
    get_genre_recommendations, hybrid_recommend
)
from search import search_movie_by_title
from poster_service import get_poster_url

@st.cache_data(show_spinner=False)
def load_context() -> Tuple[pd.DataFrame, Tuple, pd.DataFrame, pd.DataFrame]:
    movies_df, ratings, users = load_data()
    cosine_sim, indices = build_similarity_matrix(movies_df)
    return movies_df, (cosine_sim, indices), ratings, users


def _render_movie_row(title: str, genres: str, year: int, similarity_score: float = None):
    """Render movie với poster và thông tin"""
    cols = st.columns([1, 3, 1])
    poster = get_poster_url(title, year)
    
    with cols[0]:
        if poster:
            st.image(poster, width=120)
        else:
            st.empty()
    
    with cols[1]:
        st.subheader(title)
        meta = []
        if year and not pd.isna(year):
            meta.append(f"📅 {int(year)}")
        if genres:
            meta.append(f"🎭 {genres}")
        st.caption(" • ".join(meta))
    
    with cols[2]:
        if similarity_score is not None:
            st.metric("Similarity", f"{similarity_score:.1%}")

def show_genre_analysis(movies_df):
    """Hiển thị phân tích thể loại"""
    st.subheader("📊 Genre Analysis")
    
    # Tách và đếm genres
    all_genres = []
    for genres_str in movies_df['genres'].dropna():
        genres = [g.strip() for g in genres_str.split() if g.strip() != 'unknown']
        all_genres.extend(genres)
    
    genre_counts = Counter(all_genres)
    top_genres = dict(genre_counts.most_common(10))
    
    # Tạo bar chart đơn giản
    df_genres = pd.DataFrame(list(top_genres.items()), columns=['Genre', 'Count'])
    st.bar_chart(df_genres.set_index('Genre'))

def show_year_distribution(movies_df):
    """Hiển thị phân bố năm phát hành"""
    st.subheader("📈 Movies by Year")
    
    # Lọc năm hợp lệ
    valid_years = movies_df[movies_df['year'].notna() & (movies_df['year'] > 1900)]['year']
    year_counts = valid_years.value_counts().sort_index()
    
    st.line_chart(year_counts)

def create_user_profile():
    """Tạo user profile cho hybrid recommendations"""
    st.sidebar.subheader("🎯 Your Preferences")
    
    # Favorite genres
    available_genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Adventure']
    selected_genres = st.sidebar.multiselect(
        "Favorite Genres", 
        available_genres,
        default=['Action', 'Comedy']
    )
    
    # Year range
    year_range = st.sidebar.slider(
        "Preferred Year Range",
        min_value=1920,
        max_value=2000,
        value=(1980, 2000)
    )
    
    return {
        'genres': selected_genres,
        'year_range': year_range
    }

def main():
    st.set_page_config(page_title="🎬 Movie Recommender", page_icon="🎬", layout="wide")
    
    # Header
    st.title("🎬 Advanced Movie Recommender")
    st.markdown("*Discover movies you'll love using AI-powered recommendations*")
    
    # Load data
    movies_df, (cosine_sim, indices), ratings, users = load_context()
    
    # Sidebar navigation
    st.sidebar.title("🎮 Navigation")
    page = st.sidebar.selectbox(
        "Choose a feature:",
        ["🔍 Movie Search & Recommend", "🎭 Browse by Genre", "📊 Dataset Analytics", "🎯 Hybrid Recommendations"]
    )
    
    if page == "🔍 Movie Search & Recommend":
        # Original search functionality với cải tiến
        st.header("Search & Recommend Movies")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            q = st.text_input("🔍 Enter movie title:", value="Toy Story", placeholder="e.g., Toy Story, Titanic, etc.")
        
        with col2:
            topn = st.slider("Number of recommendations", min_value=3, max_value=20, value=8)
        
        search_btn = st.button("🚀 Search & Recommend", type="primary")
        
        if search_btn and q.strip():
            # Search results
            results = search_movie_by_title(q, movies_df, top_n=10)
            if results.empty:
                st.warning("❌ No matching movies found. Try a different title!")
                return
            
            st.success(f"✅ Found {len(results)} matching movies")
            
            # Show search results
            with st.expander("📋 Search Results", expanded=True):
                for _, row in results.iterrows():
                    _render_movie_row(row["title"], row["genres"], row["year"])
            
            # Recommendations
            seed_title = results.iloc[0]["title"]
            st.header(f"🎯 Because you searched: *{seed_title}*")
            
            recs = recommend(seed_title, movies_df, cosine_sim, indices, top_n=topn, return_scores=True)
            
            if not recs.empty:
                for _, row in recs.iterrows():
                    similarity = row.get('similarity_score', None)
                    _render_movie_row(row["title"], row["genres"], row["year"], similarity)
            else:
                st.info("No recommendations found for this movie.")
    
    elif page == "🎭 Browse by Genre":
        st.header("Browse Movies by Genre")
        
        # Genre selection
        popular_genres = ['Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller', 'Adventure', 'Animation']
        
        col1, col2 = st.columns(2)
        with col1:
            selected_genre = st.selectbox("Choose a genre:", popular_genres)
        with col2:
            num_movies = st.slider("Number of movies", 5, 20, 10)
        
        if st.button("🎭 Find Movies"):
            genre_movies = recommend_by_genres(movies_df, [selected_genre], top_n=num_movies)
            
            if not genre_movies.empty:
                st.success(f"Found {len(genre_movies)} {selected_genre} movies")
                
                for _, row in genre_movies.iterrows():
                    score = row.get('genre_score', 1)
                    _render_movie_row(row["title"], row["genres"], row["year"], score/max(genre_movies['genre_score']))
            else:
                st.warning(f"No {selected_genre} movies found!")
    
    elif page == "📊 Dataset Analytics":
        st.header("Dataset Analytics & Insights")
        
        # Basic stats
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Movies", f"{len(movies_df):,}")
        
        with col2:
            st.metric("Total Ratings", f"{len(ratings):,}")
        
        with col3:
            st.metric("Total Users", f"{len(users):,}")
        
        with col4:
            avg_rating = ratings['rating'].mean()
            st.metric("Avg Rating", f"{avg_rating:.1f}/5")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            show_genre_analysis(movies_df)
        
        with col2:
            show_year_distribution(movies_df)
    
    elif page == "🎯 Hybrid Recommendations":
        st.header("Personalized Hybrid Recommendations")
        st.info("Combine content-based filtering with your personal preferences!")
        
        # User preferences
        user_prefs = create_user_profile()
        
        # Movie input
        movie_title = st.text_input("Enter a movie you like:", value="Toy Story")
        num_recs = st.slider("Number of recommendations", 5, 15, 10)
        
        if st.button("🎯 Get Personalized Recommendations"):
            if movie_title.strip():
                hybrid_recs = hybrid_recommend(
                    movie_title, movies_df, cosine_sim, indices, 
                    user_preferences=user_prefs, top_n=num_recs
                )
                
                if isinstance(hybrid_recs, str):
                    st.error(hybrid_recs)
                elif not hybrid_recs.empty:
                    st.success("🎉 Here are your personalized recommendations!")
                    
                    for _, row in hybrid_recs.iterrows():
                        final_score = row.get('final_score', row.get('similarity_score', 0))
                        _render_movie_row(row["title"], row["genres"], row["year"], final_score)
                else:
                    st.warning("No recommendations found!")
    
    # Footer
    st.markdown("---")
    st.markdown("*Powered by MovieLens 100K Dataset & Content-Based Filtering*")


if __name__ == "__main__":
    main()


