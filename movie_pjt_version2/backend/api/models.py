from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import time
from django.utils import timezone
import json

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default='M')
    age = models.IntegerField(default=25)
    occupation = models.CharField(max_length=200)
    username = models.CharField(max_length=100, default="DDoromi")
    subscription = models.DateTimeField(default=timezone.now)


#  wrapper for create user Profile
def create_profile(**kwargs):
    user = User.objects.create_user(
        username=kwargs['username'],
        password=kwargs['password'],
        is_active=True,
    )

    profile = Profile.objects.create(
        user=user,
        username=kwargs['username'],
        gender=kwargs['gender'],
        age=kwargs['age'],
        occupation=kwargs['occupation']
    )
    return profile


class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    genres = models.CharField(max_length=500)
    average_rating = models.FloatField(default=0)
    total_rater = models.IntegerField(default=1)
    views_count = models.IntegerField(default=0)
    description = models.TextField(default='')
    released = models.TextField(default='')
    runtime = models.TextField(default='')
    director = models.TextField(default='')
    actors = models.TextField(default='')
    country = models.TextField(default='')
    poster = models.TextField(default='')
    ratings = models.TextField(default='')

    male = models.IntegerField(default=0)
    female = models.IntegerField(default=0)

    age10 = models.IntegerField(default=0)  # 0 ~ 19
    age20 = models.IntegerField(default=0)  # 20 ~ 29
    age30 = models.IntegerField(default=0)  # 30 ~ 39
    age40 = models.IntegerField(default=0)  # 40 ~
    job00 = models.IntegerField(default=0)
    job01 = models.IntegerField(default=0)
    job02 = models.IntegerField(default=0)
    job03 = models.IntegerField(default=0)
    job04 = models.IntegerField(default=0)
    job05 = models.IntegerField(default=0)
    job06 = models.IntegerField(default=0)
    job07 = models.IntegerField(default=0)
    job08 = models.IntegerField(default=0)
    job09 = models.IntegerField(default=0)
    job10 = models.IntegerField(default=0)
    job11 = models.IntegerField(default=0)
    job12 = models.IntegerField(default=0)
    job13 = models.IntegerField(default=0)
    job14 = models.IntegerField(default=0)
    job15 = models.IntegerField(default=0)
    job16 = models.IntegerField(default=0)
    job17 = models.IntegerField(default=0)
    job18 = models.IntegerField(default=0)
    job19 = models.IntegerField(default=0)
    job20 = models.IntegerField(default=0)

    @property
    def genres_array(self):
        return self.genres.strip().split('|')

    @property
    def ratings_dict(self):
        ratings = self.ratings
        if ratings == '[]' or len(ratings) == 3:
            return {}
        ratings = ratings[1:-1].replace("},", "}|")
        ratings = ratings.split('|')
        result = dict()
        for rating in ratings:
            _result = json.loads(rating.replace("'", "\""))
            result[_result['Source']] = _result['Value']
        return result

    @property
    def seen_users(self):
        return list(map(lambda rating: [rating.user.username,rating.user.id], self.rating_set.all()))


def update_movie_view_count(**kwargs):
    movie = Movie.objects.get(id=kwargs['movie_id'])
    movie.views_count += 1
    movie.save()


def update_movie_auth(**kwargs):
    user = User.objects.get(id=kwargs['user_id'])
    movie = Movie.objects.get(id=kwargs['movie_id'])
    movie.users.add(user)


class MovieClustering(models.Model):
    movie = models.OneToOneField(Movie, on_delete=models.CASCADE)
    GMM_labels = models.IntegerField(default=0)
    HIE_labels = models.IntegerField(default=0)
    KMeans_labels = models.IntegerField(default=0)
    Custom_labels = models.IntegerField(default=0)


def create_movie_clustering(**kwargs):
    movie = Movie.objects.get(
        id=kwargs["movie_id"]
    )
    movie_clustering = MovieClustering.objects.create(
        movie=movie,
        GMM_labels=kwargs["GMM_labels"],
        HIE_labels=kwargs["HIE_labels"],
        KMeans_labels=kwargs["KMeans_labels"]
    )


class UserClustering(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    KMeans_labels = models.IntegerField(default=0)
    HIE_labels = models.IntegerField(default=0)
    GMM_labels = models.IntegerField(default=0)


def create_user_clustering(**kwargs):
    user = User.objects.get(
        id=kwargs["user_id"]
    )
    UserClustering.objects.create(
        user=user,
        KMeans_labels=kwargs["KMeans_labels"],
        HIE_labels=kwargs["HIE_labels"],
        GMM_labels=kwargs["GMM_labels"]
    )


class Rating(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.IntegerField()
    # time_stamp = models.DateTimeField(null=True)


def create_rating(**kwargs):
    user = User.objects.get(id=kwargs['user_id'])
    movie = Movie.objects.get(id=kwargs['movie_id'])
    rating = Rating.objects.create(
        user=user,
        movie=movie,
        rating=kwargs['rating_value'],
        # time_stamp=time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(int(kwargs['time_stamp']))),
    )
    return rating


class ClusteringState(models.Model):
    id = models.IntegerField(primary_key=True)
    clustering_state = models.IntegerField(default=0)


class MovieRecommendation(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    KNNRecommendation = models.TextField(default='')
    ALSRecommendation = models.TextField(default='')