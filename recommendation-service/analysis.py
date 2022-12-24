import os

frequencyCounter = {}
with open("./reports/telemetry_dataA.txt", "r") as f:
    for i in f.readlines()[:100]:
        movies = i.split(" ")[-2].split(",")[1:-2]
        for movie in movies:
            if movie in frequencyCounter:
                frequencyCounter[movie] +=1
            else:
                frequencyCounter[movie] = 1


frequencyCounterSorted = []
for key in frequencyCounter:
    frequencyCounterSorted.append((frequencyCounter[key], key))

frequencyCounterSorted.sort(reverse = True)
for i in frequencyCounterSorted:
    print(i)