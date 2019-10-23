from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import create_profile, Profile, UserClustering
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib.auth import authenticate
from api.serializers import ProfileDetailSerializer
from datetime import timedelta, datetime


@api_view(['POST'])
def signup_many(request):
    if request.method == 'POST':
        profiles = request.data.get('profiles', None)
        for profile in profiles:
            username = profile.get('username', None)
            password = profile.get('password', None)
            age = profile.get('age', None)
            occupation = profile.get('occupation', None)
            gender = profile.get('gender', None)

            create_profile(username=username, password=password, age=age,
                           occupation=occupation, gender=gender)

        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST', 'GET'])
def signup(request):
    if request.method == 'POST':
        profile = request.data.get('profile', None)
        username = profile.get('username', None)
        password = profile.get('password', None)
        age = profile.get('age', None)
        occupation = profile.get('occupation', None)
        gender = profile.get('gender', None)
        create_profile(username=username, password=password, age=age, occupation=occupation, gender=gender)
        user = User.objects.get(username=username)
        UserClustering.objects.create(user=user)
        return Response(status=status.HTTP_201_CREATED)

    if request.method == 'GET':
        username = request.GET.get('username', None)
        users = User.objects.all()
        is_duplicated = False
        for user in users:
            if user.username == username:
                is_duplicated = True
                break
        return JsonResponse({'isDuplicated': is_duplicated})


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        profile = request.data.get('profile', None)
        username = profile.get('username', None)
        password = profile.get('password', None)
        # 아이디 및 비밀번호 확인
        user = authenticate(username=username, password=password)
        # 남은 구독 일수(second)
        remaining_subscription = user.profile.subscription - datetime.now()
        is_expired = remaining_subscription.total_seconds() < 0

        return JsonResponse({
            'status': True if user else False,
            'user': {
                "id": user.id if user else None,
                "username": user.username if user else None,
                "is_expired": is_expired,
                "gender": user.profile.gender if user else None,
                "age": user.profile.age if user else None,
                "occupation": user.profile.occupation if user else None,
                "subscription": user.profile.subscription if user else None,
                "is_staff": user.is_staff if user else None,
                "is_superuser": user.is_superuser if user else None,
            }
        })


@api_view(['POST'])
def update_profile(request):
    if request.method == 'POST':
        profile = request.data.get('profile', None)
        id = profile.get('id', None) # user_id
        #TODO: username 변경 가능하게 할 것인지? 한다면 중복검사 과정 필요
        new_gender = profile.get('gender', None)
        new_age = profile.get('age', None)
        new_occupation = profile.get('occupation', None)
        new_subscription = profile.get('subscription', None)
        new_is_staff = profile.get('is_staff', None)
        new_is_superuser = profile.get('is_superuser')
        user = User.objects.filter(id=id)
        # 잘못된 user_id일 경우
        if not user:
            return JsonResponse({
                "status": False,
                "profile": None,
                "message": "일치하는 유저가 없습니다."
            })
        user = user[0]
        profile = user.profile
        if new_gender:
            profile.gender = new_gender
        if new_age:
            profile.age = new_age
        if new_occupation:
            profile.occupation = new_occupation
        if new_subscription > 0:
            profile.subscription += timedelta(days=new_subscription)
        elif new_subscription == 0:
            profile.subscription = datetime.now()
        remaining_subscription = profile.subscription - datetime.now()
        is_expired = remaining_subscription.total_seconds() < 0
        profile.save()
        return JsonResponse({
            "status": True,
            "profile": {
                "id": profile.id,
                "username": profile.username,
                "is_expired": is_expired,
                "gender": profile.gender,
                "age": profile.age,
                "occupation": profile.occupation,
                "subscription": profile.subscription,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser
            },
            "message": "유저정보가 변경됐습니다."
        })