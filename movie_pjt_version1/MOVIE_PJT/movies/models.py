from django.db import models
from accounts.models import User
# Create your models here.

#
# class Genre(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f'{self.id}: {self.name}'
#
#
# class Nation(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f'{self.id}: {self.name}'
#
#
# class Grade(models.Model):
#     name = models.CharField(max_length=20)
#
#     def __str__(self):
#         return f'{self.id}: {self.name}'

# 영화코드, 영화명(국문), 영화명(영문), 상영시간, 상영국가, 영화장르,
# 감독1명, 배우3명, 영화상영등급, 누적관객수, 개봉일, 이미지url, 줄거리, 예고편url
class Movie(models.Model):
    movie_cd = models.CharField(max_length=20, blank=True, null=True)
    title_ko = models.CharField(max_length=100, blank=True, null=True)
    title_en = models.CharField(max_length=100, blank=True, null=True)
    movie_tm = models.CharField(max_length=50, blank=True, null=True)
    nation = models.CharField(max_length=50, blank=True, null=True)
    genre = models.CharField(max_length=50, blank=True, null=True)
    director = models.CharField(max_length=100, blank=True, null=True)
    actor1 = models.CharField(max_length=100, blank=True, null=True)
    actor2 = models.CharField(max_length=100, blank=True, null=True)
    actor3 = models.CharField(max_length=100, blank=True, null=True)
    grade = models.CharField(max_length=50, blank=True, null=True)
    audience = models.CharField(max_length=100, blank=True, null=True)
    open_dt = models.CharField(max_length=100, blank=True, null=True)
    poster_url = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    trailer_url = models.TextField(blank=True, null=True)
    score_sum = models.IntegerField(default=0)
    average_score = models.FloatField(default=0)

    class Meta:
        ordering=['-average_score']

    # def __str__(self):
    #     return f'{self.id}: {self.title_ko[:20]}'

class Score(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    value = models.IntegerField()


    class Meta:
        ordering=['-value']

    # def __str__(self):
    #     return f'{self.movie.title_ko}: {self.value}, {self.content[:30]}'
