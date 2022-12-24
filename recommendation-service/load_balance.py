import sys
import os
from flask import jsonify
from flask import Response
from flask import Flask
import pickle
import json
from flask import request, make_response
import requests
import numpy as np
import random
import time
import datetime
from influxdb import InfluxDBClient
# coding=utf8

app = Flask('load-balancer-server')

probability = 0.7

def checkHealth(ip_addr):
    return os.system('nc -vz '+ip_addr) == 0

@app.route("/recommend/<userid>")
def welcome(userid):
    # add health check
    A_server_up = checkHealth('0.0.0.0 7004')
    B_server_up = checkHealth('0.0.0.0 7005')

    client = InfluxDBClient(host="128.2.205.109",port="8086")
    client.switch_database("grafana_monitoring")

    if not B_server_up and A_server_up:
        response = requests.get(f'http://0.0.0.0:7004/recommend/{userid}')
    elif B_server_up and not A_server_up:
        response = requests.get(f'http://0.0.0.0:7005/recommend/{userid}')
    elif A_server_up and B_server_up:
        #print(userid,'this is number')
        if int(userid)%2 == 0:
            start = time.time()
            response = requests.get(f'http://0.0.0.0:7004/recommend/{userid}').text
            #print('this is response ', response)
            done = time.time()
            now = datetime.datetime.now() # current date and time
            date_time = now.strftime(" %m/%d/%Y:%H:%M:%S")
            elapsed = done - start
            with open("./reports/telemetry_dataA.txt", "a") as f:
            # Writing data to a file
                print('writing sumthing')
                f.write('userid '+ userid+','+ 'time'+(date_time) + ','+str(response) + ',inference '+str(elapsed)+"\n")
            
            json_data = [{"measurement":"LatencyTimesA","time":datetime.datetime.utcnow(),"fields":{"latency":elapsed}}]
            client.write_points(json_data)
        else:
            start = time.time()
            response= requests.get(f'http://0.0.0.0:7005/recommend/{userid}').text
            
            done = time.time()
            now = datetime.datetime.now() # current date and time
            date_time = now.strftime(" %m/%d/%Y:%H:%M:%S")
            elapsed = done - start
            with open("./reports/telemetry_dataB.txt", "a") as f:
            # Writing data to a file
                print('writing sumthing')
                f.write('userid '+ userid+ ','+ 'time'+(date_time) + ','+str(response) + ',inference '+str(elapsed)+"\n")

            json_data = [{"measurement":"LatencyTimesB","time":datetime.datetime.utcnow(),"fields":{"latency":elapsed}}]
            client.write_points(json_data)
    else:
        response = ''
    return Response(response, mimetype='text/plain')

if __name__ == '__main__':
    from waitress import serve
    serve(app, host="0.0.0.0", port=8082, backlog=2048)
