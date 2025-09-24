import os
from typing import List, Tuple

import pandas as pd
import streamlit as st

from data_loader import load_data
from recommend import build_similarity_matrix, recommend
from search import search_movie_by_title
from poster_service import get_poster_url


@st.cache_data(show_spinner=False)
def load_context():
    movies_df, ratings, users = load_data()
    cosine_sim, indices = build_similarity_matrix(movies_df)
    return movies_df, (cosine_sim, indices)


def _render_movie_row(title: str, genres: str, year):
    cols = st.columns([1, 3])
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
            meta.append(str(int(year)))
        if genres:
            meta.append(genres)
        st.caption(" • ".join(meta))


def main():
    st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")
    st.title("🎬 Movie Recommender")
    st.caption("Search a film, then get similar recommendations with posters.")

    movies_df, (cosine_sim, indices) = load_context()

    with st.sidebar:
        st.header("Search")
        q = st.text_input("Movie title", value="Toy Story")
        topn = st.slider("Number of recommendations", min_value=3, max_value=20, value=8)
        search_btn = st.button("Search & Recommend", type="primary")

    if search_btn and q.strip():
        results = search_movie_by_title(q, movies_df, top_n=10)
        if results.empty:
            st.warning("No matching movies found.")
            return

        st.subheader("Search results")
        for _, row in results.iterrows():
            _render_movie_row(row["title"], row["genres"], row["year"]) 

        # Recommend based on the first result
        seed_title = results.iloc[0]["title"]
        st.divider()
        st.subheader(f"Because you searched: {seed_title}")
        recs = recommend(seed_title, movies_df, cosine_sim, indices, top_n=topn)
        
        # Display recommendations safely
        if isinstance(recs, pd.DataFrame) and not recs.empty:
            for _, row in recs.iterrows():
                # Safely get year from movies_df by matching title
                year_match = movies_df[movies_df['title'] == row['title']]
                year = year_match['year'].iloc[0] if not year_match.empty else None
                _render_movie_row(row["title"], row.get("genres", ""), year)


if __name__ == "__main__":
    main()


