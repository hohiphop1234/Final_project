# main.py
from data_loader import load_data, save_processed
from search import get_movie_data, search_movie_by_title
from recommend import build_similarity_matrix, recommend

def main():
    movies_df, ratings, users = load_data()
    save_processed(movies_df, ratings, users)
    
    print(search_movie_by_title("Toy Story", movies_df))
    print(get_movie_data(1, movies_df))
    
    cosine_sim, indices = build_similarity_matrix(movies_df)
    print(recommend("Toy Story", movies_df, cosine_sim, indices, top_n=5))

if __name__ == "__main__":
    main()
