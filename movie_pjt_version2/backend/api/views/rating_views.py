from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Rating
from api.models import create_rating, Rating, User, Movie
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
def ratings(request):
	if request.method == 'GET':
		user_id = request.GET.get('user_id')
		movie_id = request.GET.get('movie_id')
		user = None
		movie = None
		if user_id:
			user = User.objects.filter(id=user_id)
			if user:
				user = user[0]
		if movie_id:
			movie = Movie.objects.filter(id=movie_id)
			if movie:
				movie = movie[0]

		# 특정 user 의 특정 movie 평점
		if movie_id and user_id:
			if not user or not movie:
				return JsonResponse({
					"status": False,
					"message": "일치하는 유저 또는 영화가 없습니다."
				})
			rating = Rating.objects.filter(user=user, movie=movie)
			return JsonResponse({
				"status": True,
				"rating_id": rating[0].id if rating else None,
				"rating_value": rating[0].rating if rating else None
			})

		# 특정 movie 의 모든 평점
		elif movie_id:
			if not movie:
				return JsonResponse({
					"status": False,
					"message": "일치하는 영화가 없습니다."
				})
			rating_set = []
			ratings = Rating.objects.filter(movie=movie)
			for rating in ratings:
				user = rating.user
				rating_set.append({
					"rating_id": rating.id,
					"user_id": user.id,
					"user_name": user.username,
					"movie_id": movie.id,
					"rating_value": rating.rating
				})
			return JsonResponse({
				"status": True,
				"ratings": rating_set
			})

		# 특정 user 의 모든 평점
		elif user_id:
			if not user:
				return JsonResponse({
					"status": False,
					"message": "일치하는 유저가 없습니다."
				})
			rating_set = []
			ratings = Rating.objects.filter(user=user)
			for rating in ratings:
				movie = rating.movie
				rating_set.append({
					"rating_id": rating.id,
					"user_id": user.id,
					"movie_id": movie.id,
					"movie_title": movie.title,
					"movie_poster": movie.poster,
					"rating_value": rating.rating
				})
			return JsonResponse({
				"status": True,
				"ratings": rating_set
			})
		# user, movie 가 모두 존재하지 않을 때
		else:
			return JsonResponse({
				"status": False,
				"message": "조건과 일치하는 평점이 존재하지 않습니다."
			})

	elif request.method == "POST":
		ratings = request.data.get('ratings', None)
		for rating in ratings:
			user_id = rating.get('user_id', None)
			movie_id = rating.get('movie_id', None)
			rating_value = rating.get('rating_value', None)
			time_stamp = rating.get('time_stamp', None)
			create_rating(user_id=user_id, movie_id=movie_id, rating_value=rating_value, time_stamp=time_stamp)
		return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
def create_or_update_rating(request):
	if request.method == "POST":
		rating = request.data.get('rating', None)
		user_id = rating.get('user_id')
		movie_id = rating.get('movie_id')
		rating_value = rating.get('rating_value')
		user = get_object_or_404(User, id=user_id)
		movie = get_object_or_404(Movie, id=movie_id)
		movie_total_rating = movie.average_rating * movie.total_rater  # 영화 총 평점 = 평균평점 * 평가자 수

		rating = Rating.objects.filter(movie=movie, user=user)
		# update
		if rating:
			rating = rating[0]
			movie_total_rating -= rating.rating  # 기존 평점
			rating.rating = rating_value
			rating.save()
		# create
		else:
			rating = Rating.objects.create(movie=movie, user=user, rating=rating_value)
			movie.total_rater += 1

		movie_total_rating += rating_value  # 새로운 평점
		movie.average_rating = round(movie_total_rating / movie.total_rater, 2)
		movie.save()

		return JsonResponse({
			"status": True if rating else False,
			"message": "평점이 생성 또는 수정됐습니다." if rating else "일치하는 영화 또는 유저가 없습니다."
		})