import requests
import datetime
import sys
from influxdb import InfluxDBClient
client = InfluxDBClient(host="128.2.205.109",port="8086")
client.switch_database("grafana_monitoring")
while(True):
    
    try:
        res = requests.get('http://128.2.205.109:8082/recommend/7')
        if res.status_code==200:
            #print(1)
            json_data = [{"measurement":"Availability","time":datetime.datetime.utcnow(),"fields":{"avail":1}}]
        else:
            json_data = [{"measurement":"Availability","time":datetime.datetime.utcnow(),"fields":{"avail":0}}]
            #print(0)
        client.write_points(json_data)
    except KeyboardInterrupt:
        sys.exit(1)
    except:
        json_data = [{"measurement":"Availability","time":datetime.datetime.utcnow(),"fields":{"avail":0}}]
        client.write_points(json_data)