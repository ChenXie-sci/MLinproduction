#from app import app
from flask import make_response
from flask import Flask
import time
import pandas as pd
import os
import datetime
from recommendation_model import model_process
from functools import lru_cache
from pathlib import Path
import pickle
import argparse

# coding=utf8

app = Flask(__name__)
#This route serves the user recommendations
@app.route("/recommend/<userid>")
@lru_cache
def recommend(userid):
    start = time.time()
    myList=list(model_process.gettop20movies(userid, app.algo, app.df_new))
    moviesID=[]
    moviedata = []
    for x in myList:
        for k in x['Movie']:
            raw_string = x['Movie'][k]
            moviesID.append(raw_string.split('/rate/')[1].split('=')[0])
            moviedata.append(raw_string)
    print(moviesID)
    response = make_response(",".join(moviesID), 200)
    response.mimetype = "text/plain"
    done = time.time()
    elapsed = done - start
    #print('writing sumthing proceeding')
    # Writing to file
    with open("./reports/telemetry_data.txt", "a") as f:
    # Writing data to a file
        print('writing sumthing')
        f.write(",".join(moviedata)+str(elapsed)+"\n")
    return response#, moviedata}


@app.errorhandler(404)
def error(error):
    # Writing to telemetry file containing timestamps when the service had error
    with open(os.getcwd()+"/reports/telemetry_downtime.txt", "a") as f:
    # Writing current timestamp to a file
        f.write(str(datetime.datetime.now())+"\n")
    return "This page does not exist :("

def main(args):
    app.run(host='0.0.0.0', port=8081, debug=False)

if __name__ == '__main__':
    #Flask('demo-movie-server')
    d = str(Path().resolve())

    parser = argparse.ArgumentParser()

    parser.add_argument('-modelpath','--m', default= "./recommendation_model/finalized_model.pkl")
    #parser.add_argument('--telepath', 't', default = "./reports/telemetry_time.txt")

    args = parser.parse_args()

    app.df_new = pd.read_csv(d +"/recommendation_model/" + '/newrate_movie.csv', nrows=50)
    app.df_new['id'] = range(0, len(app.df_new))
    filet = open(args.modelpath,'rb')
    app.algo = pickle.load(filet)

    main(args)




