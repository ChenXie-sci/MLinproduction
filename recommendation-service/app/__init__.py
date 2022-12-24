from flask import Flask
import pandas as pd
from pathlib import Path
import pickle


app = Flask(__name__)

'''
Preloading data to improve performance
'''
d = str(Path().resolve())

app.df_new = pd.read_csv(d +"/recommendation_model/" + '/newrate_movie.csv', nrows=50)
app.df_new['id'] = range(0, len(app.df_new))

filet = open(d +"/recommendation_model/" + "/finalized_model.pkl",'rb')
app.algo = pickle.load(filet)

from app import views