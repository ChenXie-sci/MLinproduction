import os
import random
import time
import requests

def getRecommendation(userId):
    start = time.time()
    response = requests.get("http://128.2.205.109:8082/recommend/"+str(userId))
    stop = time.time()
    
    return stop - start

def mean():
    sum = 0 
    count = 0
    with open(os.getcwd()+"/reports/telemetry_time.txt", "r") as f:
        sum = sum + float(f.readline())
        count+=1
    
    return sum/count

    
    

if __name__ == '__main__':
    if os.path.getsize(os.getcwd()+"/reports/telemetry_time.txt") < 10:
        for i in range(100):
            randomid = random.randint(10, 900000)
            with open(os.getcwd()+"/reports/telemetry_time.txt", "a") as f:
                f.write(str(getRecommendation(randomid))+"\n")
                f.close()
    with open(os.getcwd()+"/reports/telemetry_latency_mean.txt", "w") as f:
        f.write("Average Latency: " + str(mean())+" seconds \n")
        f.close()