from rest_framework import status
from rest_framework.decorators import api_view
from api.models import Movie, update_movie_view_count, MovieClustering
from api.serializers import MovieSerializer, MovieDetailSerializer
from rest_framework.response import Response
import random
from django.http import JsonResponse


@api_view(['GET', 'POST', 'DELETE'])
def movies(request):
    if request.method == 'GET':
        id = request.GET.get('id', request.GET.get('movie_id', None))
        isUpdateRating = request.GET.get('isUpdateRating', None)
        title = request.GET.get('title', None)
        genres = request.GET.get('genres', None)
        sortBy = request.GET.get('sortBy', None)
        sortingBy = request.GET.get('sortingBy', None)
        agesItems = ["-ㅤ","0~19", "20~29", "30~39", "40~"]
        genderItems = ["-ㅤㅤ", "Male", "Female"]

        movies = Movie.objects.all()

        if id and isUpdateRating:
            movies = movies.filter(pk=id)
            serializer = MovieDetailSerializer(movies, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if id:
            movies = movies.filter(pk=id)
            update_movie_view_count(movie_id=id)
            serializer = MovieDetailSerializer(movies, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        if title:
            movies = movies.filter(title__icontains=title)
        if genres:
            if genres == "All":
                genres = ""
            movies = movies.filter(genres__icontains=genres)
        if sortBy:
            if sortBy == "조회순":
                movies = movies.order_by('-views_count')
            elif sortBy == "평점순":
                movies = movies.order_by('-average_rating')
        if sortingBy:
            if sortingBy in agesItems:
                if sortingBy =="0~19":
                    movies = sorted(movies, key=lambda i: i.age10/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
                elif sortingBy =="20~29":
                    movies = sorted(movies, key=lambda i: i.age20/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
                elif sortingBy == "30~39":
                    movies = sorted(movies, key=lambda i: i.age30/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
                elif sortingBy == "40~":
                    movies = sorted(movies, key=lambda i: i.age40/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
                else:
                    movies = Movie.objects.all()
            elif sortingBy in genderItems:
                if sortingBy == "Male":
                    movies = sorted(movies, key=lambda i: i.male/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
                elif sortingBy =="Female":
                    movies = sorted(movies, key=lambda i: i.female/(i.total_rater if i.total_rater!=0 else 1), reverse=True)
            else:
                occupation_map = {'other': 0, 'academic/educator': 1, 'artist': 2, 'clerical/admin': 3, 'college/grad student': 4,
                 'customer service': 5, 'doctor/health care': 6, 'executive/managerial': 7, 'farmer': 8, 'homemaker': 9,
                 'K-12 student': 10, 'lawyer': 11, 'programmer': 12, 'retired': 13, 'sales/marketing': 14, 'scientist': 15,
                 'self-employed': 16, 'technician/engineer': 17, 'tradesman/craftsman': 18, 'unemployed': 19, 'writer': 20}
                index = "job" + (str(occupation_map[sortingBy]) if len(str(occupation_map[sortingBy])) != 1 else "0" + str(occupation_map[sortingBy]))
                movies = sorted(movies, key=lambda i: getattr(i,index) / (i.total_rater if i.total_rater != 0 else 1), reverse=True)

        serializer = MovieSerializer(movies, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        movie = Movie.objects.all()
        movie.delete()
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        movies = request.data.get('movies', None)
        for movie in movies:
            id = movie.get('id', None)
            title = movie.get('title', None)
            genres = movie.get('genres', None)

            if not (id and title and genres):
                continue
            if Movie.objects.filter(id=id).count() > 0 or Movie.objects.filter(title=title).count() > 0:
                continue

            Movie(id=id, title=title, genres='|'.join(genres)).save()

        return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
def get_movie_recommendation(request):
    if request.method == 'GET':
        movie_id = request.GET.get('movie_id', None)
        fit = request.GET.get('fit', None)  # 알고리즘 기준 현재의 경우 k-means
        movie = Movie.objects.get(id=movie_id)
        movie_clustering = movie.movieclustering  # User Clustering object
        label = getattr(movie_clustering, fit)
        # 해당 cluster label 에 속한 다른 user_set 추출하기
        _clusters = MovieClustering.objects.filter(KMeans_labels=label)
        clusters = []
        for _ in range(100):
            a = random.choice(_clusters)
            if a not in clusters and len(clusters) < 10:
                clusters.append(a)
        recommendation_set = []
        for cluster in clusters:
            movie = Movie.objects.get(id=cluster.movie_id)
            recommendation_set.append({
                "id": movie.id,
                "title": movie.title
            })
        return JsonResponse({
            'recommendation_set': recommendation_set
        })
