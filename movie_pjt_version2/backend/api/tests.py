from .models import *
from django.contrib.auth.models import User
import pandas as pd
from sklearn.cluster import KMeans
import requests
import json
from bigdata_modules.ALS2_MF import alsmain
from bigdata_modules.KNN_userbased import knnmain


def create_movie_init():
    movies = pd.read_csv('../data/movies.dat', sep="::", engine='python', header=None)
    df_records = movies.to_dict("records")
    model_instance = [
        Movie(
            id=record[0],
            title=record[1],
            genres=record[2],
        ) for record in df_records]
    Movie.objects.bulk_create(model_instance)


def create_user_init():
    occupation_map = {
        0: "other", 1: "academic/educator", 2: "artist", 3: "clerical/admin", 4: "college/grad student",
        5: "customer service", 6: "doctor/health care", 7: "executive/managerial", 8: "farmer", 9: "homemaker",
        10: "K-12 student", 11: "lawyer", 12: "programmer", 13: "retired", 14: "sales/marketing",
        15: "scientist", 16: "self-employed", 17: "technician/engineer", 18: "tradesman/craftsman",
        19: "unemployed", 20: "writer"
    }
    users = pd.read_csv('../data/users.dat', sep="::", engine='python', header=None)

    for i in range(len(users.index)):
        username = "user" + str(users.loc[i][0])
        password = username
        gender = users.loc[i][1]
        age = int(users.loc[i][2])
        occupation = occupation_map[int(users.loc[i][3])]
        create_profile(username=username, password=password, age=age, occupation=occupation, gender=gender)
        print(i, "/6040")
    else:
        print("create user done")
        print("create rating start 10분가량 걸림")


def create_movie_description():
    text1 = pd.read_csv('../data/ml_plot.dat', sep="::", engine='python', header=None)
    for id in range(1, 3953):
        text2 = text1.loc[text1[0] == id]
        if not text2.empty:
            movie = Movie.objects.get(id=text2.values[0][0])
            movie.description = text2.values[0][1].replace('\t', ' ').replace(' |', '.')
            movie.save()


def create_movie_information():
    for id in range(1, 3953):
        movie = Movie.objects.filter(id=id)
        if len(movie) == 0:
            continue
        movie = movie[0]
        title = movie.title.split()
        title.pop()
        res = requests.get('http://www.omdbapi.com/?t={}&apikey=5d30c8ea'.format(title))
        print(id, res)
        information = json.loads(res.text)
        if information['Response'] == 'True':
            information = json.loads(res.text)
            movie.released = information['Released']
            movie.runtime = information['Runtime']
            movie.director = information['Director']
            movie.actors = information['Actors']
            movie.country = information['Country']
            movie.poster = information['Poster']
            movie.ratings = information['Ratings']
            if movie.description == '':
                movie.description = information['Plot']
            movie.save()

def create_movie_information_to_database():
    movies = pd.read_csv('../data/movie_information.tsv', sep="\t", engine='python', header=None)
    for i in movies.T:
        movie_id = movies.loc[i][0]
        movie = Movie.objects.get(id=movie_id)
        movie.released = movies.loc[i][39]
        movie.runtime = movies.loc[i][40]
        movie.director = movies.loc[i][36]
        movie.actors = movies.loc[i][34]
        movie.country = movies.loc[i][35]
        movie.poster = movies.loc[i][37]
        movie.ratings = movies.loc[i][38]
        movie.description = movies.loc[i][33]
        movie.save()
        print(i)




def create_rating_init():
    ratings = pd.read_csv('../data/ratings.dat', sep="::", engine='python', header=None)
    df_records = ratings.to_dict("records")
    print(1, "rating")
    model_instance = [
        Rating(
            rating=record[2],
            movie_id=record[1],
            user_id=record[0],
        ) for record in df_records]
    print(2, "rating")
    Rating.objects.bulk_create(model_instance)
    print(3, "rating")


def pandas_cheating_average_input_and_other():
    rating_data = pd.read_csv('../data/ratings.dat', sep="::", engine='python', header=None)
    user_data = pd.read_csv('../data/users.dat', sep="::", engine='python', header=None)
    print(1, "cheating")
    for idse in range(1, 3953):
        temp_user_or = rating_data[rating_data[1] == idse][2]
        dataval = [0] * 29
        dataval[28] = sum(x for x in temp_user_or)
        temp_user = rating_data[rating_data[1] == idse][0]
        for ind, val in user_data[1][list(temp_user)].value_counts().iteritems():
            if ind == "M":
                dataval[1] = val
            elif ind == "F":
                dataval[2] = val

        for ind, val in user_data[2][list(temp_user)].value_counts().iteritems():
            if 0 <= ind <= 19:
                dataval[3] += val
            elif 20 <= ind <= 29:
                dataval[4] += val
            elif 30 <= ind <= 39:
                dataval[5] += val
            elif 40 <= ind:
                dataval[6] += val

        for ind, val in user_data[3][list(temp_user)].value_counts().iteritems():
            dataval[int(ind) + 7] += val

        dataval[0] = sum(dataval[1:3])
        oneMovie = Movie.objects.filter(id=idse)
        if oneMovie:
            oneMovie = oneMovie[0]
            oneMovie.total_rater = dataval[0]
            oneMovie.male = dataval[1]
            oneMovie.female = dataval[2]
            oneMovie.age10 = dataval[3]
            oneMovie.age20 = dataval[4]
            oneMovie.age30 = dataval[5]
            oneMovie.age40 = dataval[6]
            oneMovie.job00 = dataval[7]
            oneMovie.job01 = dataval[8]
            oneMovie.job02 = dataval[9]
            oneMovie.job03 = dataval[10]
            oneMovie.job04 = dataval[11]
            oneMovie.job05 = dataval[12]
            oneMovie.job06 = dataval[13]
            oneMovie.job07 = dataval[14]
            oneMovie.job08 = dataval[15]
            oneMovie.job09 = dataval[16]
            oneMovie.job10 = dataval[17]
            oneMovie.job11 = dataval[18]
            oneMovie.job12 = dataval[19]
            oneMovie.job13 = dataval[20]
            oneMovie.job14 = dataval[21]
            oneMovie.job15 = dataval[22]
            oneMovie.job16 = dataval[23]
            oneMovie.job17 = dataval[24]
            oneMovie.job18 = dataval[25]
            oneMovie.job19 = dataval[26]
            oneMovie.job20 = dataval[27]
            if len(temp_user_or) != 0:
                oneMovie.average_rating = round(dataval[28] / len(temp_user_or), 2)
            oneMovie.save()
    else:
        print("create pandas cheating done")
        print("start create movie label 10분가량걸림")


def create_movie_label():
    movie_label_schema = pd.read_csv("../data/movie_result.csv").fillna(-1)
    for i in movie_label_schema.index:
        one_movie = movie_label_schema.loc[i]
        # if one_movie["GMM_labels"] == -1:
        create_movie_clustering(
            movie_id=int(one_movie["title"]),
            GMM_labels=int(one_movie["GMM_labels"]),
            HIE_labels=int(one_movie["HIE_labels"]),
            KMeans_labels=int(one_movie["KMeans_labels"]),
        )
    else:
        print("create create_movie_label done")
        print("start create user label 10분가량걸림")


def create_user_label():
    user_label_schema = pd.read_csv("../data/labeled_user.csv").fillna(-1)
    for i in user_label_schema.index:
        user = user_label_schema.loc[i]
        create_user_clustering(
            user_id=int(user["user_id"]),
            KMeans_labels=int(user["kmeans"]),
            HIE_labels=int(user["hierarchy"]),
            GMM_labels=int(user["gaussian"]),
        )
    else:
        print("끝났어")


def update_movie_kmeans_label():
    cosine_sim = pd.read_csv('../data/cosine_sim_movie.csv', sep=",", engine='python', index_col=0)
    kmeans_movie = KMeans(n_clusters=2, random_state=0).fit(cosine_sim)
    movie_columns = list(map(int, cosine_sim.columns))
    for cluster_number in range(2):
        movie_col = list(map(lambda y: y[1], filter(lambda x: kmeans_movie.labels_[x[0]] == cluster_number ,enumerate(movie_columns))))
        for i in range(len(movie_col)//500):
            temp_movie= movie_col[i*500:i*500+500]
            MovieClustering.objects.filter(movie_id__in=temp_movie).update(Custom_labels=cluster_number)


def update_user_profile_name():
    auth_users = User.objects.all()
    for auth_user in auth_users:
        oneProfile = auth_user.profile
        oneProfile.username = auth_user.username
        oneProfile.save()

def create_movie_recommendation():
    knn_recommend = pd.read_csv('../data/knn_recommend.csv', sep=",", engine='python',header=None)
    knn_recommend.columns = ["userId","KR"]
    als_recommend = pd.read_csv('../data/als_recommend.csv', sep=",", engine='python',header=None)
    als_recommend.columns = ["userId","AR"]
    print(als_recommend)
    sum_recommend = knn_recommend.merge(als_recommend, on="userId")
    print(sum_recommend)
    df_records = sum_recommend.to_dict("records")
    print(df_records)
    model_instance = [
        MovieRecommendation(
            user_id=record["userId"],
            KNNRecommendation=record["KR"],
            ALSRecommendation=record["AR"],
        ) for record in df_records]
    MovieRecommendation.objects.bulk_create(model_instance)


# __________________________________________
# create_movie_init()
# create_user_init()
# create_rating_init()
#
# pandas_cheating_average_input_and_other()
#
# create_movie_label()
# create_user_label()
# update_movie_kmeans_label()
# update_user_profile_name()
# create_movie_information_to_database()
create_movie_recommendation()
#________________________________________________
# create_movie_information()
