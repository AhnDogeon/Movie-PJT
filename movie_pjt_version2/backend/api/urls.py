from django.conf.urls import url
from api.views import movie_views
from api.views import auth_views
from api.views import rating_views
from api.views import user_views
from api.views import cluster_views

urlpatterns = [
    url('auth/signup-many/$', auth_views.signup_many, name='sign_up_many'),
    url('auth/signup/$', auth_views.signup, name='sign_up'),
    url('auth/login/$', auth_views.login, name='login'),
    url('auth/update_profile/$', auth_views.update_profile, name='update_profile'),
    url('movies/$', movie_views.movies, name='movie_list'),
    url('ratings/$', rating_views.ratings, name='rating_list'),
    url('create_or_update_rating/', rating_views.create_or_update_rating, name='create_or_update_rating'),
    # url('update_rating/', rating_views.update_rating, name='update_rating'),
    url('auth/user/$', user_views.users, name='user_detail'),
    url('cluster/$', cluster_views.cluster_info, name='cluster_info'),
    url('user_recommendation/', user_views.get_user_recommendation, name='get_user_recommendation'),
    url('movie_recommendation/', movie_views.get_movie_recommendation, name='get_movie_recommendation'),
]
