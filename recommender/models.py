from django.db import models

# Create your models here.


class Movie(models.Model):
  """

  """
  imdb_title_id = models.CharField(max_length=64, unique=True, null=False)
  original_title = models.CharField(max_length=128, null=False)
  year = models.IntegerField(null=True)
  date_published = models.DateField(null=True)
  duration = models.IntegerField(null=True)
  country = models.CharField(null=True, max_length=128)
  director = models.CharField(null=True, max_length=128)
  production_company = models.CharField(null=True, max_length=128)


class MovieVote(models.Model):
  """
  """
  movie = models.ForeignKey(Movie, on_delete=models.PROTECT, null=True)
  movie_imdb_id = models.CharField(max_length=128, null=False)
  user_key = models.CharField(max_length=16)
  rating = models.SmallIntegerField()
