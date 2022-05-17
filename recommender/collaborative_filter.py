import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import scipy.sparse
import os
import joblib
import gc

class CollaborativeFilter:

    def __init__(self):
        # **NOTE**: The create_project_data_file.ipynb file should be run prior if it has not been run yet.
        print("Initializing Collaborative Filter...")
        # min number of ratings required by a user in order to be included in the data set
        # Somewhere between 50 and 2000 is sufficient. 
        # The lower the number, the longer the file will take to create.
        min_user_ratings= 2000
        # Re-create collaborative filter data files 
        force = False

        # Load user_ratings and IMDB movie data
        imdb_df = pd.read_csv("project_data.csv")
        self.__user_ratings = pd.read_csv("user_likes_data.csv")
        self.__movies = imdb_df[["movieId", "imdb_title_id", "original_title"]]
        self.__user_ratings = self.__user_ratings[self.__user_ratings.groupby("userId")["userId"].transform('size') >= min_user_ratings]
        self.__user_ratings = self.__movies[["movieId"]].merge(self.__user_ratings, on="movieId", how="left")

        # Load movie_similarities dense matrix
        self.__movie_similarities = self.__create_movie_similarities_csr(force=force).todense()

        # No longer needed after similarity matrix is created
        # Release from memory
        del imdb_df
        del self.__user_ratings
        gc.collect()

        print("Collaborative Filter Load Complete\n")


    def __get_movies_by_imdb_ids(self, movieIds):
        return self.__movies[self.__movies['imdb_title_id'].isin(movieIds)]


    def __create_user_movie_likes_csr(self, ext="full", force=False):
        # Create the sparse matrix for user_movie_likes if it does not exists
        # else load from file
        csr_file_name = f"csr_user_movie_likes_{ext}.npz"
        csr_user_movie_likes = None
        if force or (not os.path.exists(csr_file_name)):
            # pivot likes into movie user matrix
            user_movie_likes = self.__user_ratings.pivot(
                index='movieId',
                columns='userId',
                values='like'
            ).fillna(0)
            csr_user_movie_likes = csr_matrix(user_movie_likes.values)
            scipy.sparse.save_npz(csr_file_name, csr_user_movie_likes)
        else:
            csr_user_movie_likes = scipy.sparse.load_npz(csr_file_name)
            print(f"Loaded Sparse User Movie Likes From {csr_file_name}...")
        
        return csr_user_movie_likes


    def __create_movie_similarities_csr(self, ext="full", force=False):
        # Create the sparse matrix for movie_similarities if it does not exists
        # else load from file
        csr_file_name = f"csr_movie_similarities_{ext}.npz"
        csr_movie_similarities = None
        if force or (not os.path.exists(csr_file_name)):
            # Sparse matrix for user movie likes
            csr_user_movie_likes = self.__create_user_movie_likes_csr(force=force)

            # create sparse similarity matrix
            csr_movie_similarities = cosine_similarity(csr_user_movie_likes,dense_output=False)
            # save csr to file
            scipy.sparse.save_npz(csr_file_name, csr_movie_similarities)
        else:
            csr_movie_similarities = scipy.sparse.load_npz(csr_file_name)
            print(f"Loaded Sparse Movie Similarities From {csr_file_name}...")
        return csr_movie_similarities


    def top_n_similar_movies(self, liked_movie_ids, disliked_movie_ids, skipped_movie_ids, n_results=1):
        # Get indexes for passed in movie_ids
        liked_movie_indexes = self.__get_movies_by_imdb_ids(liked_movie_ids).index
        disliked_movie_indexes = self.__get_movies_by_imdb_ids(disliked_movie_ids).index
        skipped_movie_indexes = self.__get_movies_by_imdb_ids(skipped_movie_ids).index

        # Aggregate similarity scores per movie
        movie_sim_agg = np.sum(self.__movie_similarities[liked_movie_indexes], axis=0).A1

        # Get all movie_indexes and sim scores where movie is not in user's "liked" list
        movie_scores = { movie_index: movie_sim
                        for movie_index, movie_sim in enumerate(movie_sim_agg)
                        if (movie_index not in liked_movie_indexes) and 
                           (movie_index not in disliked_movie_indexes) and 
                           (movie_index not in skipped_movie_indexes) and
                           (movie_sim > 0)
                       }
    
        # Sort by highest score and set top n
        sorted_scores = sorted(movie_scores.items(), key=lambda x: x[1], reverse=True)[:n_results]
    
        recommendations = [
                {
                    "imdb_title_id": self.__movies.iloc[movie_index]["imdb_title_id"],
                    "original_title": self.__movies.iloc[movie_index]["original_title"],
                    "score": movie_sim 
                }
                for movie_index, movie_sim in sorted_scores
            ]


        return recommendations
