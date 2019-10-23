from rest_framework import status
from rest_framework.decorators import api_view
from api.serializers import ProfileDetailSerializer, ProfileSerializer
from api.models import Profile, UserClustering
from django.contrib.auth.models import User
from rest_framework.response import Response
import random
from django.http import JsonResponse


@api_view(['GET', 'POST', 'DELETE'])
def users(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if id:
            user = Profile.objects.filter(id=id)
            serializer = ProfileDetailSerializer(user, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            user = Profile.objects.all()
            serializer = ProfileSerializer(user, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_user_recommendation(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id', None)
        fit = request.GET.get('fit', None) # 알고리즘 기준 현재의 경우 k-means
        user = User.objects.get(id=user_id)
        user_clustering = user.userclustering  # User Clustering object
        label = getattr(user_clustering, fit)
        # 해당 cluster label 에 속한 다른 user_set 추출하기
        _clusters = UserClustering.objects.filter(KMeans_labels=label)
        clusters = []
        for i in range(10):
            clusters.append(random.choice(_clusters))
        recommendation_set = []
        for cluster in clusters:
            user = User.objects.get(id=cluster.user_id)
            recommendation_set.append({
                "id": user.id,
                "username": user.username
            })
        return JsonResponse({
            'recommendation_set': recommendation_set
        })

