from .models import Profile, Movie, Rating
from rest_framework import serializers


class ProfileDetailSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    username = serializers.SerializerMethodField('get_username')
    is_staff = serializers.SerializerMethodField('get_is_staff')
    seen_movies = serializers.SerializerMethodField('get_movielist')
    seen_movies_id = serializers.SerializerMethodField('get_movielist_id')
    knn_recommend = serializers.SerializerMethodField('get_knn_recommend')
    als_recommend = serializers.SerializerMethodField('get_als_recommend')

    class Meta:
        model = Profile
        fields = ('id', 'username', 'is_staff', 'gender', 'age', 'occupation', 'subscription', 'seen_movies', 'seen_movies_id','knn_recommend','als_recommend')

    def get_knn_recommend(self, obj):
        result = []
        for mid in obj.user.movierecommendation.KNNRecommendation.split("/"):
            onemovie = {}
            onemovie["movieId"] = int(mid)
            onemovie["title"] = Movie.objects.get(id=int(mid)).title
            result.append(onemovie)
        return result
    def get_als_recommend(self, obj):
        result = []
        for mid in obj.user.movierecommendation.ALSRecommendation.split("/"):
            onemovie = {}
            onemovie["movieId"] = int(mid)
            onemovie["title"] = Movie.objects.get(id=int(mid)).title
            result.append(onemovie)
        return result

    def get_username(self, obj):
        return obj.user.username

    def get_is_staff(self, obj):
        return obj.user.is_staff

    def get_movielist(self, obj):
        return list(map(lambda x: x.movie.title, obj.user.rating_set.all()))

    def get_movielist_id(self, obj):
        return list(map(lambda y: y.movie.id, obj.user.rating_set.all()))


class ProfileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('id', 'username', 'gender', 'age', 'occupation', 'subscription')



class MovieSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', "average_rating", 'views_count')


class MovieDetailSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()
    ratings_dict = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array', 'average_rating', 'views_count', 'seen_users',
                  'description', 'released', 'runtime', 'director', 'actors', 'country', 'poster', 'ratings_dict')


class RatingSerializer(serializers.ModelSerializer):
    genres_array = serializers.ReadOnlyField()

    class Meta:
        model = Movie
        fields = ('id', 'title', 'genres_array')
