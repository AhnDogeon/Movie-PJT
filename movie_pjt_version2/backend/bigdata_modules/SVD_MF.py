import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
from scipy.sparse import csr_matrix

if __name__ == '__main__':
    r_lambda = 40
    nf = 200
    alpha = 40
    movies = pd.read_csv("../../data/movies.dat", sep="::", engine='python', header=None)
    Ratings = pd.read_csv("../../data/ratings.dat", sep="::", engine='python', header=None)
    Ratings.columns = ["userId", "movieId", "rating", "timestamp"]
    movies.columns = ["movieId", "title", "genres"]
    final = pd.pivot_table(Ratings, values='rating', index='userId', columns='movieId').fillna(0).values
    final_csr = csr_matrix(final)
    # final = np.array([[0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    #               [0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0],
    #               [0, 3, 4, 0, 3, 0, 0, 2, 2, 0, 0],
    #               [0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0],
    #               [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
    #               [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 5],
    #               [0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 4],
    #               [0, 0, 0, 0, 0, 0, 5, 0, 0, 5, 0],
    #               [0, 0, 0, 3, 0, 0, 0, 0, 4, 5, 0]])

    u, s, vh = np.linalg.svd(final_csr, full_matrices=True)
    print(u)
    print(s)
    print(vh)


    # predict_errors, confidence_errors, regularization_list, total_losses = train()