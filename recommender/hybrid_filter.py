from .collaborative_filter import CollaborativeFilter
from .content_filter import ContentFilter

class HybridFilter:

    def __init__(self):
        print("Initializing Hybrid Filter...")
       
        self.__collaborative_filter = CollaborativeFilter()
        self.__content_filter = ContentFilter()
        
        print("Hybrid Filter Load Complete\n")
    
    def __get_kmeans_collaborative_intersections(self, liked_movie_ids, top_collab_movies_ids):
        k_means_movie_ids = self.__content_filter.get_kmeans_movie_ids_at_intersection(liked_movie_ids)
        return list(set(k_means_movie_ids) & set(top_collab_movies_ids))
        


    def get_top_recommendation(self, liked_movie_ids, disliked_movie_ids, skipped_movie_ids):
        top_collab_movies = self.__collaborative_filter.top_n_similar_movies(liked_movie_ids, disliked_movie_ids, skipped_movie_ids, n_results=25)
        top_collab_movie_ids = [movie['imdb_title_id'] for movie in top_collab_movies]
        kmeans_collaborative_intersections = self.__get_kmeans_collaborative_intersections(liked_movie_ids, top_collab_movie_ids)

        if(len(kmeans_collaborative_intersections) > 0):
            return [movie for movie in top_collab_movies if movie["imdb_title_id"] == kmeans_collaborative_intersections[0]][0]
        else:
            return top_collab_movies[0]
