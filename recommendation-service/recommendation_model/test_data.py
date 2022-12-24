import os
import pandas as pd
import numpy as np

file = open('rate.txt')

data = pd.DataFrame(columns = ['Date', 'Number', 'Movie', 'moviename', 'rate'])
c = 0
for line in file:
    t = list(line.split(','))
    #print(t)

    t.append(t[-1].split('/')[2])
    
    if 'rate' in t[-2].split('/')[1]:
        #print(t[-2].split('/')[1])
        t.append(int(t[-2].split('=')[-1]))
    else:
        t.append(None)

    data.loc[len(data)] = t
    
#df = pd.read_csv('main_movie.csv')

#data = pd.concat([data, df])

data.to_csv('newrate_movie.csv', mode='a', header=not os.path.exists("newrate_movie.csv"))

print(len(data))
print(data['rate'].unique())
print(data.loc[0]['Movie'])