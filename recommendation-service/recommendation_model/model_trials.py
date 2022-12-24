import pandas as pd
import numpy as np
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import cross_validate
from surprise import NormalPredictor
from surprise import KNNBasic
from surprise import KNNWithMeans
from surprise import KNNWithZScore
from surprise import KNNBaseline
from surprise import SVD
from surprise import BaselineOnly
from surprise import SVDpp
from surprise import NMF
from surprise import SlopeOne
from surprise import CoClustering
from surprise.accuracy import rmse
from surprise import accuracy
import pickle
from surprise import dump
from surprise.model_selection import train_test_split

import time
import os

if __name__ == '__main__':
    ts = time.time()

    df= pd.read_csv('newrate_movie.csv')

    #df['rate'] = np.random.randint(1, 6, df.shape[0])
    start = time.time()
    print(df['Number'][0])

    name = df['moviename'].unique().tolist()

    #df['moviename'].replace(name, np.random.randint(1, len(df['moviename'].unique()), len(df['moviename'].unique())))

    min_movie_ratings = 10
    filter_movies = df['moviename'].value_counts() > min_movie_ratings
    filter_movies = filter_movies[filter_movies].index.tolist()

    min_user_ratings = 10
    filter_users = df['Number'].value_counts() > min_user_ratings
    filter_users = filter_users[filter_users].index.tolist()

    df_new = df[(df['moviename'].isin(filter_movies)) & (df['Number'].isin(filter_users))]
    print('The original data frame shape:\t{}'.format(df.shape))
    print('The new data frame shape:\t{}'.format(df_new.shape))


    # ratings_dict = {"item" : df['moviename'].tolist(),
    #                 "user" : df['Number'].tolist(),
    #                 "rating": df['rate'].tolist()}

    #df = pd.DataFrame(ratings_dict)
    reader = Reader(rating_scale=(0, 5))

    # Loads Pandas dataframe
    data = Dataset.load_from_df(df_new[["Number", "moviename", "rate"]], reader)

    #“rmse” as our accuracy metric for the predictions.

    benchmark = []
    # Iterate over all algorithms
    for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF(), NormalPredictor(), KNNBaseline(), KNNBasic(), KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
        # Perform cross validation
        results = cross_validate(algorithm, data, measures=['RMSE'], cv=3, verbose=False)
        
        # Get results & append algorithm name
        tmp = pd.DataFrame.from_dict(results).mean(axis=0)
        tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))
        benchmark.append(tmp)

    #algo = KNNWithMeans(sim_options=sim_options)

    # Train
    #trainingSet = data.build_full_trainset()
    #algo.fit(trainingSet)

    surprise_results = pd.DataFrame(benchmark).set_index('Algorithm').sort_values('test_rmse')

    print(surprise_results)

    print('Using ')
    bsl_options = {'n_epochs': 5,
                'reg_u': 12,
                'reg_i': 5
                }
    algo = NMF()
    cross_validate(algo, data, measures=['MSE'], cv=3, verbose=False)

    trainset, testset = train_test_split(data, test_size=0.25)
    algo1 = NMF()
    predictions = algo1.fit(trainset).test(testset)
    algo1.fit(trainset)
    #dump.dump('./finalized_modelB.pkl', predictions, algo)
    pickle.dump(algo1, open( './finalized_modelA.pkl', 'wb'))

    algo2 = CoClustering()
    predictions = algo2.fit(trainset).test(testset)
    algo2.fit(trainset)
    #dump.dump('./finalized_modelB.pkl', predictions, algo)
    pickle.dump(algo2, open( './finalized_modelB.pkl', 'wb'))

    accuracy.rmse(predictions)
    done = time.time()
    elapsed = done - start
    with open("../reports/training_report.txt", "a") as f:
                    f.write("Timestamp: " + str(ts) + " " + "Time taken to train (seconds): " + str(elapsed) +"\n")
                    f.close()


    # Predict
    #prediction = algo.predict(118971, 1)
    #print (prediction.est)
