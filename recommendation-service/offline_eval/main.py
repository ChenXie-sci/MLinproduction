from validationdata_curation import *
from model_evaluation import *
import os
import argparse
import numpy as np
import pandas as pd
#import pytest

##Test the Randomly Generated Data
## pytest for test, magic library for python


def test_traintestplit():
    df = pd.read_csv('newrate_movie.csv')
    vl = ValidationData(df)
    vl.data_preprocess()

    val = vl.data_drift()

    assert len(val) >= 0
    previous = len(val)

    val = vl.low_distributed_data()

    assert len(val) >= previous

    val = vl.regression_testing()

    
    assert len(val) >= previous

    train = vl.traindata_curation()

    return val, train

def test_checkvaldata():
        val, train = test_traintestplit()
        assert len(val) > 50
        msg = 'same id present in val and train'

        assert len(train) > 1000

        for id in val['Number']:
            if id in train['Number'].values:
                raise pytest.UsageError(msg)


def test_modeleval():
        val, train = test_traintestplit()
        assert len(train) > 0 

        ma = ModelAccuracy(train)

        ma.ModelSelection()
        ma.FinalTraining()


# if __name__ == '__main__':

#     test = checkAllTests('newrate_movie.csv')

#     #print(test.head())

#     test.test_traintestplit()

#     test.test_checkvaldata()

#     test.test_modeleval()






    
