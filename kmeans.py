import random
import math
import copy
from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

class Point(object):
    def __init__(self, rowid, title, year, duration, *args, **kwargs):
        self.rowid = rowid
        # values
        self.id = rowid
        self.title = title
        self.year = year
        self.duration = duration
        self.Action = kwargs.get('Action', 0)
        self.Adventure = kwargs.get('Adventure', 0)
        self.Animation = kwargs.get('Animation', 0)
        self.Biography = kwargs.get('Biography', 0)
        self.Film_Noir = kwargs.get('Film_Noir', 0)
        self.History = kwargs.get('History', 0)
        self.Horror = kwargs.get('Horror', 0)
        self.Music = kwargs.get('Music', 0)
        self.Musical = kwargs.get('Musical', 0)
        self.Mystery = kwargs.get('Mystery', 0)
        self.Romance = kwargs.get('Romance', 0)
        self.Sci_Fi = kwargs.get('Sci_Fi', 0)
        self.Sport = kwargs.get('Sport', 0)
        self.Thriller = kwargs.get('Thriller', 0)
        self.War = kwargs.get('War', 0)
        self.Western = kwargs.get('Western', 0)
        
    
    def __repr__(self):
        # So we can see the data and everything that's happening
        return "Point<{},{},{}>".format(self.title, self.year, self.duration)
    
    def get_values(self):
        return (self.duration, self.Action, self.Adventure, self.Animation, self.Biography, self.Film_Noir, self.History, self.Horror, self.Music, self.Musical,
            self.Mystery, self.Romance, self.Sci_Fi, self.Sport, self.Thriller, self.War, self.Western)
    
    def calculate_distance(self, point):
        """
        Calculates the Euclidean distance between two points
        """
        self_values = np.array(self.get_values())
        other_point_values = np.array(point.get_values())
        #import pdb; pdb.set_trace()
        return (np.sqrt(np.sum(np.square(self_values - other_point_values) , axis = 0)))

class Cluster():
    def __init__(self, centroid=None, points=[]):
        self.id = random.randint(3020,500000)
        self.centroid = centroid
        self.points = points

    def __repr__(self):
        return "Centroid id:{} w/ Centroid {}".format(str(self.id), str(self.centroid))

    def calculate_sse(self):
        # Generates an SSE for a cluster using distrance from centroid
        SSE = 0
        for p in self.points:
            SSE = SSE + p.calculate_distance(self.centroid)
        return SSE
    
    def get_mean_point_values(self):
        # Get the new centroid point
        means = [0,0,0,0]
        if len(self.points) == 0:
            return Point(*means)
        distances = []
        for p in self.points:
            self.centroid.calculate_distance(self.centroid, p)
        min_index = np.amin(distances)
        # Set the new centroid
        self.centroid = self.points[min_index]
        return self.centroid

    def generate_centroid(self):
        # Generates a new centroid by using a mean point to get the best fit point for the mean values
        distances = []
        for p in self.points:
            distances.append(p.get_values())
        d_arr = np.array(distances)
        average = np.average(d_arr, axis = 0)
        print(average)
        # Set the new centroid
    
        self.centroid = Point(
            0, "Centroid", 2020,
            duration=average[0], Action=average[1], Adventure=average[2], Animation=average[3], Biography=average[4],
            Film_Noir=average[5], History=average[6], Horror=average[7], Music=average[8],
            Musical=average[9], Mystery=average[10], Romance=average[11], Sci_Fi=average[12],
            Sport=average[13], Thriller=average[14], War=average[15], Western=average[16],
        )
        return self.centroid


all_points = []
# Split up arrays

df = pd.read_csv('project_data_w_labels.csv')
for i,movie in df.iterrows():
    point = Point( i, movie['original_title'], movie['year'], movie['duration'], Action=movie['Action'],
    Animation=movie['Animation'], Biography=movie['Biography'], Film_Noir=movie['Film-Noir'], History=movie['History'], Horror=movie['Horror'],
    Music=movie['Music'], Musical=movie['Musical'], Mystery=movie['Mystery'], Romance=movie['Romance'], Sci_Fi=movie['Sci-Fi'],
    Sport=movie['Sport'], Thriller=movie['Thriller'], War=movie['War'], Western=movie['Western'])
    all_points.append(point)

def calc_kmeans(K=2):
    # randomly select K points to generate clusters from
    copied_points = copy.deepcopy(all_points)
    clusters = [ Cluster(centroid=copied_points[random.randint(0, len(copied_points) - 1)], points=[]) for c in range(0,K)]
    print("Amount of Clusters: {}".format(len(clusters)))
    # initial assignment to cluster
    for p in copied_points:
        closest_cluster = clusters[0]
        cluster_dist = closest_cluster.centroid.calculate_distance(p)
        for clus in clusters:
            distance = clus.centroid.calculate_distance(p)
            if p.id == clus.centroid.id:
                closest_cluster = clus
                break
            if distance < cluster_dist:
                closest_cluster = clus
        closest_cluster.points.append(p)
    # now for each cluster get the find a better centroid till no change
    overall_sse = 0
    for cluster in clusters:
        import pdb; pdb.set_trace()
        print(cluster.centroid)
        cluster.generate_centroid()
        sse = cluster.calculate_sse()
        overall_sse = overall_sse + sse
        print("Amount of Points in Cluster: {}".format(len(cluster.points)))
        print("Cluster {} SSE: {}".format(cluster.id, sse))
    return overall_sse
    
calc_kmeans(K=20)
