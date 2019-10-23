import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import pairwise_distances


def find_n_neighbours(df, n):
    order = np.argsort(df.values, axis=1)[:, :n]
    df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
                                      .iloc[:n].index,
                                      index=['top{}'.format(i) for i in range(1, n + 1)]), axis=1)
    return df


def get_user_similar_movies(user1, user2):
    common_movies = Rating_avg[Rating_avg.userId == user1].merge(
        Rating_avg[Rating_avg.userId == user2],
        on="movieId",
        how="inner")
    return common_movies.merge(movies, on='movieId')


def User_item_score1(user):
    Movie_seen_by_user = check.columns[check[check.index == user].notna().any()].tolist()
    a = sim_user_30_m[sim_user_30_m.index == user].values
    b = a.squeeze().tolist()
    d = Movie_user[Movie_user.index.isin(b)]
    l = ','.join(d.values)
    Movie_seen_by_similar_users = l.split(',')
    Movies_under_consideration = list(set(Movie_seen_by_similar_users) - set(list(map(str, Movie_seen_by_user))))
    Movies_under_consideration = list(map(int, Movies_under_consideration))
    score = []
    for item in Movies_under_consideration:
        c = final_movie.loc[:, item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['userId'] == user, 'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_movie.loc[user, index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score', 'correlation']
        fin['score'] = fin.apply(lambda x: x['adg_score'] * x['correlation'], axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume / deno)
        score.append(final_score)
    data = pd.DataFrame({'movieId': Movies_under_consideration, 'score': score})
    top_5_recommendation = data.sort_values(by='score', ascending=False).head(5)
    Movie_Name = top_5_recommendation.merge(movies, how='inner', on='movieId')
    Movie_Names = Movie_Name.movieId.values.tolist()
    return Movie_Names

def knnmain():
    global movies,final_movie,Mean,similarity_with_movie,sim_user_30_m,Movie_user,check,Rating_avg
    movies = pd.read_csv("../data/movies.dat", sep="::", engine='python', header=None)
    Ratings = pd.read_csv("../data/ratings.dat", sep="::", engine='python', header=None)
    Ratings.columns = ["userId", "movieId", "rating", "timestamp"]
    movies.columns = ["movieId", "title", "genres"]

    Mean = Ratings.groupby(by="userId", as_index=False)['rating'].mean()
    Rating_avg = pd.merge(Ratings, Mean, on='userId')
    Rating_avg['adg_rating'] = Rating_avg['rating_x'] - Rating_avg['rating_y']
    final = pd.pivot_table(Rating_avg, values='adg_rating', index='userId', columns='movieId')
    final_movie = final.fillna(final.mean(axis=0))
    final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
    check = pd.pivot_table(Rating_avg, values='rating_x', index='userId', columns='movieId')

    b = cosine_similarity(final_user)
    np.fill_diagonal(b, 0)
    similarity_with_user = pd.DataFrame(b, index=final_user.index)
    similarity_with_user.columns = final_user.index

    cosine = cosine_similarity(final_movie)
    np.fill_diagonal(cosine, 0)
    similarity_with_movie = pd.DataFrame(cosine, index=final_movie.index)
    similarity_with_movie.columns = final_user.index

    sim_user_30_m = find_n_neighbours(similarity_with_movie, 10)
    Rating_avg = Rating_avg.astype({"movieId": str})
    Movie_user = Rating_avg.groupby(by='userId')['movieId'].apply(lambda x: ','.join(x))
    result = {}
    for i in sim_user_30_m.index:
        result[i] = "/".join(map(str,User_item_score1(i)))
        print(i)

    resultDF = pd.DataFrame.from_dict(result, orient='index')
    resultDF.columns = ["recommend_movie"]
    resultDF.to_csv("knn_recommend.csv", mode='w')
    # return result
if __name__ == "__main__":
    knnmain()
