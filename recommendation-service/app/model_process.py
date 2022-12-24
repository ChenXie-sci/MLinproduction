import os
import argparse
from surprise import dump
from surprise import Reader
from surprise import NMF
import pandas as pd
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise.model_selection import cross_validate
import difflib
import random
import pickle

from pathlib import Path

def get_movie_id(movie_title, metadata):
    
    existing_titles = list(metadata['moviename'].values)
    closest_titles = difflib.get_close_matches(movie_title, existing_titles)
    movie_id = metadata[metadata['moviename'] == closest_titles[0]]['id'].values[0]
    return movie_id

def get_movie_info(movie_id, metadata):
    
    movie_info = metadata[metadata['id'] == movie_id][['Movie']]
    return movie_info.to_dict()

def predict_review(user_id, movie_title, model, metadata):
    
    movie_id = get_movie_id(movie_title, metadata)
    review_prediction = model.predict(uid=user_id, iid=movie_id)
    return review_prediction.est

def generate_recommendation(user_id, model, metadata, thresh=1):
    count = 0
    final_list = []
    movie_titles = list(metadata['moviename'].values)
    random.shuffle(movie_titles)
    
    for movie_title in movie_titles:
        rating = predict_review(user_id, movie_title, model, metadata)
        if rating >= thresh and count < 20:
            movie_id = get_movie_id(movie_title, metadata)
            final_list.append(get_movie_info(movie_id, metadata))
            count += 1
        else:
            return final_list

#User facing method
def gettop20movies(user_id, algo, df_new):
    
    parser = argparse.ArgumentParser(description = 'Movie recommendations ')
    parser.add_argument('--ID', '-i', type = int, default = 15531)
    parser.add_argument('--movie', '-m', type = str, default = 'foon')
    parser.add_argument('--rate', '-r', type= int, default=5)

    args = parser.parse_args()
    args.ID = user_id
    
    reader = Reader(rating_scale=(0, 5))

    args.algo = algo
    args.df_new = df_new
    return generate_recommendation(args.ID, args.algo, args.df_new)

if __name__ == '__main__':
    pass




