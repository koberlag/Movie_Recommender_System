import pandas as pd
import gc



class ContentFilter:

    def __init__(self):
        print("Initializing Content Filter...")
       
        self.k_means_clusters = {}
        self.__load_k_means_clusters()
        
        print("Content Filter Load Complete\n")

    def __load_k_means_clusters(self):
        # Load k-means clusters from file
        kmeans_df = pd.read_csv("project_data_kmeans_labels.csv")

        for i,row in kmeans_df.iterrows():
            self.k_means_clusters[row["label"]] = self.k_means_clusters.get(row["label"], [])
            self.k_means_clusters[row["label"]].append(row["imdb_title_id"])

        # No longer needed after clusters are created
        # Release from memory
        del kmeans_df
        gc.collect()
    
    def get_kmeans_movie_ids_at_intersection(self, liked_movie_ids):
        # For the given list of liked movie ids,
        # find the clusters that contain movieIds that intersect the liked movie ids list.
        # Return all movie ids from each cluster that has an intersection.
        user_cluster_movie_ids = set()
        for key, movie_ids in self.k_means_clusters.items():
            if (bool(set(liked_movie_ids) & set(movie_ids))):
                # An intersection exists
                # Add all movies ids for the cluster to user_cluster_movie_ids
                user_cluster_movie_ids.update(movie_ids)
            
        return user_cluster_movie_ids

