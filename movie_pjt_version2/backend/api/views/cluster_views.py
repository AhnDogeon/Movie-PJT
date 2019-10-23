from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
import codecs
from copy import deepcopy
import numpy as np
from api.models import MovieClustering

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import linkage
from scipy.cluster.hierarchy import fcluster
from sklearn.mixture import GaussianMixture

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def cluster_info(request):
    if request.method == 'GET':
        foo = int(request.GET.get('foo', None))
        algorithm = request.GET.get('selectedAlgorithm', None)
        print(foo, algorithm)
        if algorithm=="KNN" or algorithm=="MatrixFactorization":
            result_val = {}
            if algorithm=="KNN":
                result = pd.read_csv('../data/knn_recommend.csv', sep=",", engine='python',header=None)
                result.columns = ["userId","recommendMovie"]
                df_records = result.to_dict("records")
                result_val["name"] = "KNN"
                result_val["result"] = df_records
            else:
                result = pd.read_csv('../data/als_recommend.csv', sep=",", engine='python',header=None)
                result.columns = ["userId","recommendMovie"]
                df_records = result.to_dict("records")
                result_val["name"] = "ALS"
                result_val["result"] = df_records
            return Response(result_val, status=status.HTTP_201_CREATED)

        cosine_sim = pd.read_csv('../data/cosine_sim_movie.csv', sep=",", engine='python', index_col=0)
        movie_columns = list(map(int, cosine_sim.columns))
        if algorithm == "Kmeans clustering":
            kmeans_movie = KMeans(n_clusters=foo, random_state=0).fit(cosine_sim)
            clusters = kmeans_movie.labels_
            print(clusters)
        elif algorithm == "handmade Kmeans clustering":
            clusters = kmeans_algorithm(foo, cosine_sim.values)
        elif algorithm == "Hierarchical clustering":
            max_d = 1000
            Z = linkage(cosine_sim, 'ward')
            clusters = list(map(lambda x: x-1, fcluster(Z, max_d, criterion='distance')))
        elif algorithm == "Gaussian mixture model clustering":
            gmm = GaussianMixture(n_components=foo).fit(cosine_sim)
            clusters = list(gmm.predict(cosine_sim))
        else:
            return

        result_val = {}
        for cluster_number in range(foo):
            movie_col = list(map(lambda y: y[1], filter(lambda x: clusters[x[0]] == cluster_number,
                                                        enumerate(movie_columns))))
            result_val[cluster_number] = movie_col
            print(result_val)
            for i in range(len(movie_col) // 500):
                temp_movie = movie_col[i * 500:i * 500 + 500]
                MovieClustering.objects.filter(movie_id__in=temp_movie).update(Custom_labels=cluster_number)
        else:
            return Response(result_val, status=status.HTTP_201_CREATED)

def dist(a, b, ax=1):
    return np.linalg.norm(a - b, axis=ax)


def kmeans_algorithm(cluster, array_input):
    k = cluster
    features = len(array_input[0])
    random_index = np.random.randint(0, len(array_input) - 1, size=k)
    random_list = [array_input[ri] for ri in random_index]
    C = np.array(random_list, dtype=np.float32)

    C_old = np.zeros(C.shape)
    clusters = np.zeros(len(array_input))
    error = dist(C, C_old, None)
    while error != 0:
        for i in range(len(array_input)):
            distances = dist(array_input[i], C)
            cluster = np.argmin(distances)
            clusters[i] = cluster
        C_old = deepcopy(C)

        for i in range(k):
            points = [array_input[j] for j in range(len(array_input)) if clusters[j] == i]
            C[i] = np.mean(points, axis=0)

        error = dist(C, C_old, None)
    else:
        return clusters