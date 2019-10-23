import json
import numpy as np
import requests
import pandas as pd

API_URL = 'http://localhost:8000/api/'
headers = {'content-type': 'application/json'}

def create_users(num_users):
    user_data = open('./users.dat', 'r', encoding='ISO-8859-1')
    request_data = {'profiles': []}
    occupation_map = {
        0: "other", 1: "academic/educator", 2: "artist", 3: "clerical/admin", 4: "college/grad student",
        5: "customer service", 6: "doctor/health care", 7: "executive/managerial", 8: "farmer", 9: "homemaker",
        10: "K-12 student", 11: "lawyer", 12: "programmer", 13: "retired", 14: "sales/marketing",
        15: "scientist", 16:  "self-employed", 17: "technician/engineer", 18: "tradesman/craftsman",
        19: "unemployed", 20: "writer"
    }
    user_list = []
    for line in user_data.readlines():
        [userid, gender, age, occupation, zipcode] = line.split('::')
        username = 'user' + userid
        age = int(age)
        occupation = occupation_map[int(occupation)]

        request_data['profiles'].append({
            'username': username,
            'password': username,
            'age': age,
            'gender': gender,
            'occupation': occupation
        })



        if len(request_data['profiles']) >= num_users:
            break

    response = requests.post(API_URL + 'auth/signup-many/', data=json.dumps(request_data), headers=headers)
    print(response.text)


def create_movies():
    movie_data = open('./movies.dat', 'r', encoding='ISO-8859-1')
    request_data = {'movies': []}
    for line in movie_data.readlines():
        [id, title, genres] = line.split('::')
        genres = genres[:-1].split('|')
        request_data['movies'].append({
            'id': id,
            'title': title,
            'genres': genres
        })

    response = requests.post(API_URL + 'movies/', data=json.dumps(request_data), headers=headers)
    print(response.text)


def create_ratings(num_users):
    rating_data = open('./ratings.dat', 'r', encoding='ISO-8859-1')
    request_data = {'ratings': []}
    for line in rating_data.readlines():
        [user_id, movie_id, rating, time_stamp] = line.split('::')
        if int(user_id) > num_users:
            break
        request_data['ratings'].append({
            'user_id': user_id,
            'movie_id': movie_id,
            'rating_value': rating,
            'time_stamp': time_stamp[:-2]
        })
    print(request_data)
    response = requests.post(API_URL + 'rating/', data=json.dumps(request_data), headers=headers)
    print(response.text)

def get_movie_info_by_id(movie_id):
    score_data = np.loadtxt("./ratings.dat", delimiter="::", dtype=np.str)
    # user_data = np.loadtxt("./users.dat", delimiter="::", dtype=np.str)
    # for i in range(len(user_data)):
    #     if str(i+1) != user_data[i][0]:
    #         print(i, user_data[i])
    for idse in range(3953):
        movie_schema = [0]*28
        data_for_movie_id = score_data[score_data[:, 1] == str(idse),0]
        data_con = map(lambda x:int(x)-1, data_for_movie_id)
        temp_data = user_data[list(data_con)]
        movie_schema[1] = len(temp_data[temp_data[:,1]=="M"])
        movie_schema[2] = len(temp_data[temp_data[:,1]=="F"])

    else:
        print(movie_schema)
        # for user_id in data_for_movie_id:
        #     data_movie_all = user_data[user_data[:, 0] == user_id, :][0]
        #     movie_schema[0] += 1
        #     if data_movie_all[1]=="M":
        #         movie_schema[1] += 1
        #     else:
        #         movie_schema[2] += 1
        #     if 0<=int(data_movie_all[2])<=19:
        #         movie_schema[3] += 1
        #     elif 20<=int(data_movie_all[2])<=29:
        #         movie_schema[4] += 1
        #     elif 30 <= int(data_movie_all[2]) <= 39:
        #         movie_schema[5] += 1
        #     elif 40 <= int(data_movie_all[2]):
        #         movie_schema[6] += 1
        #     movie_schema[int(data_movie_all[3])+7] += 1
        # else:
        #     print(idse)

def panda_movie():
    rating_data = pd.read_csv('./ratings.dat',sep="::",engine='python')
    rating_data.head
    # for idse in range(3953):
    #     print(rating_data[rating_data[0]==idse])
    #

if __name__ == '__main__':
    num_users = 100
    # create_movies()
    create_users(num_users)
    create_ratings(num_users)
    # get_movie_info_by_id(1)
    # panda_movie()

