from django.shortcuts import render
from .models import MovieVote
from django.http import JsonResponse
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import scipy.sparse
import os
import joblib
from .models import Movie, MovieVote
import requests
from .hybrid_filter import HybridFilter
from random import randint
from .models import Movie
from django.core import serializers


hybrid_filter = HybridFilter()


def get_vote_from_movie(request):
  user = request.user
  user_key = request.GET.get('user_key')
  movie = request.GET.get('movie_title')
  rating = request.GET.get('rating')
  MovieVote.objects.create(movie=movie, user_key=user_key, rating=rating)
  return JSONResponse({
    'success': True
  })


def load_movies_into_database(request):
  Movie.objects.all().delete()
  imdb_df = pd.read_csv("project_data.csv")
  movies = []
  id_exist = {}
  for i, row in imdb_df.iterrows():
    #import pdb; pdb.set_trace()
    movie_id = row['imdb_title_id']
    if not id_exist.get(movie_id, False):
      movies.append(Movie(imdb_title_id=movie_id, original_title=row['original_title'], year=int(row['year']), director=row['director'], production_company=row['production_company']))
      id_exist[str(movie_id)] = row
  Movie.objects.bulk_create(movies)
  return JsonResponse({
    'success': True
  })


def set_movie_vote_from_user(request):
  user_key = request.GET.get('username')
  movie_id = request.GET.get('movieId')
  rating = request.GET.get('rating')
  # If not skip
  if(rating != "0"):
    movie = Movie.objects.filter(imdb_title_id=movie_id).first()
    MovieVote.objects.create(movie=movie, movie_imdb_id=movie_id, user_key=user_key, rating=rating)
  
  return JsonResponse({
    'success': True
  })


def get_random_movies_db(request):
  movie_ids = request.GET.get('have_rated')
  data = serializers.serialize("json", Movie.objects.all())



def get_recommendation_for_user(request):
  user_key = request.GET.get('username')
  skipped_movie_ids = request.GET.get('skippedMovieIds').split(",")
  movie = {}
  liked_movie_ids = []
  disliked_movie_ids = []

  # Get user votes
  user_movie_ratings = MovieVote.objects.filter(user_key=user_key).values("movie_imdb_id", "rating")
 
  if(user_movie_ratings.exists()):
    liked_movie_ids = [umr["movie_imdb_id"] for umr in user_movie_ratings if umr["rating"] == 1]
    disliked_movie_ids = [umr["movie_imdb_id"] for umr in user_movie_ratings if umr["rating"] == -1]
  
  if(not liked_movie_ids):
    # Load random movie
    while(True):
      count = Movie.objects.all().count()
      random_index = randint(0, count - 1)
      random_movie =  Movie.objects.all()[random_index]
      if(random_movie.imdb_title_id not in disliked_movie_ids):
        movie["movieId"] = random_movie.imdb_title_id
        movie["title"] = random_movie.original_title
        break
  else:
    # If user has likes then call model
    rec_movie = hybrid_filter.get_top_recommendation(liked_movie_ids, disliked_movie_ids, skipped_movie_ids)
    movie["movieId"] = rec_movie["imdb_title_id"]
    movie["title"] = rec_movie["original_title"]

  movie_info = fetchMovieInfo(movie["movieId"])
  movie["posterUrl"] = movie_info["Poster"]

  return JsonResponse({
    'success': True,
    'movie': movie
  })




def fetchMovieInfo(movieId):
  # omdbapi
  url= f"http://www.omdbapi.com/?apikey=b1970f97&i={movieId}"
  response = requests.get(url)
  data = response.json()
  return data