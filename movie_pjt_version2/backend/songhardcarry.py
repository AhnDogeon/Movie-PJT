from .models import Profile, Movie, Rating
from rest_framework import serializers
class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.SerializerMethodField('get_username')
    is_staff = serializers.SerializerMethodField('get_is_staff')
    seen_movie = serializers.SerializerMethodField('get_movielist')
    class Meta:
        model = Profile
        fields = ('id', 'username', 'is_staff', 'gender', 'age', 'occupation', 'seen_movie')
    def get_username(self, obj):
        return obj.user.username
    def get_is_staff(self, obj):
        return obj.user.is_staff
    def get_movielist(self, obj):
        return list(map(lambda x: x.title, obj.user.movies.all()))
class MovieSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'average_rating', 'views_count')
class MovieDetailSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'average_rating', 'views_count', 'seen_users')
class RatingSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array')