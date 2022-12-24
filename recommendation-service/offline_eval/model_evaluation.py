import os
import argparse
from surprise import dump
from surprise import Reader
from surprise import NMF, BaselineOnly, CoClustering, KNNBaseline, SVD, KNNBasic, SVDpp, KNNWithZScore, KNNWithMeans, SlopeOne,NormalPredictor
import pandas as pd
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
import difflib
import random
import pickle
import numpy as np
from surprise.model_selection import GridSearchCV
import pytest


## Add pytest
##Find reduction in error - different error metrics as well 
#1) With respect to Grid Search - Hyper Parameter Tuning
#2) Different models
#3) Different types of cross validations of data. 
#4) https://www.alldatascience.com/recommender-systems/simple-recipe-recommender-system-with-scikit-surprise/


class ModelAccuracy:

    def __init__(self, testdata):
        reader = Reader(rating_scale=(0, 5))


        self.testdata = testdata
        self.testdata =  Dataset.load_from_df(self.testdata[["Number", "moviename", "rate"]], reader)

    def ModelSelection(self):
        self.benchmark = []
        for algorithm in [SVD(), SVDpp(), SlopeOne(), NMF()]:#,  KNNBasic()]:#, KNNWithMeans(), KNNWithZScore(), BaselineOnly(), CoClustering()]:
            # Perform cross validation
            results = cross_validate(algorithm, self.testdata, measures=['RMSE'], cv=3, verbose=False)
            print(results)
            # Get results & append algorithm name
            tmp = pd.DataFrame.from_dict(results).mean(axis=0)
            tmp = tmp.append(pd.Series([str(algorithm).split(' ')[0].split('.')[-1]], index=['Algorithm']))

            self.benchmark.append(tmp)

        self.surprise_results = pd.DataFrame(self.benchmark)#.set_index('Algorithm').sort_values('test_rmse')

        assert len(self.surprise_results) > 0

        print(self.surprise_results)

    def CrossValidate(self, k):
        cross_validate(self.algo, self.testdata, measures=['RMSE', 'MAE'], cv=k, verbose=True)
    
    def ParameterTuning(self):
        param_grid = {'n_factors': [100,150],
              'n_epochs': [20,25,30],
              'lr_all':[0.005,0.01,0.1],
              'reg_all':[0.02,0.05,0.1]}
        grid_search = GridSearchCV(SVD, param_grid, measures=['rmse','mae'], cv=3)
        grid_search.fit(self.testdata)     
        print(grid_search.best_params['rmse'])

        self.results_df = pd.DataFrame.from_dict(grid_search.cv_results)

    def FinalTraining(self):
        idx  = np.where(self.surprise_results['test_time'] == min(self.surprise_results['test_time']))[0]#self.surprise_results[['test_time']].idxmin()
        #self.final_params = self.results_df.iloc[idx]['params']
        
        assert self.surprise_results.iloc[idx[0]]['test_time'] == min(self.surprise_results['test_time'])

        assert self.surprise_results.iloc[idx[0]]['test_rmse'] < 1.5

        print('Best Algorithm is ', self.surprise_results.iloc[idx[0]]['Algorithm'])

        #self.algo = SVD(self.final_params)

    

# if __name__ == '__main__':
#     df_new= pd.read_csv('newrate_movie.csv')

#     ma = ModelAccuracy(df_new)

#     ma.ModelSelection()

#     ma.FinalTraining()

    #ma.CrossValidate(3)

    #ma.ParameterTuning()

    # Loads Pandas dataframe
   

    #filet = open("finalized_model.pkl",'rb')
    #algo = pickle.load(filet)

