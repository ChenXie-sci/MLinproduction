import pandas as pd
import random
import recmetrics


origin_data = pd.read_csv('newrate_movie.csv')
data_a = pd.read_csv('telemetry_dataA.txt')
data_b = pd.read_csv('telemetry_dataB.txt')

n1 = len(data_a.columns)
n2 = len(data_b.columns)

model1 = []
model2 = []
for i in range(2,n1):
    if (data_a.columns[i]).startswith('inference') == False:
        model1.append(data_a.columns[i])
    if (data_b.columns[i]).startswith('inference') == False:  
        model2.append(data_b.columns[i])

model1.append(data_a.columns[1].split(' ')[2])
model2.append(data_b.columns[1].split(' ')[2])

#presonalization score    
print(recmetrics.personalization([model1, model2]))

origin_data = origin_data.iloc[:100]
length = origin_data.shape[0]
dic = {}
for i in range(length):
    dic[origin_data.iloc[i]['Movie'].split('/')[2][:-3]] = origin_data.iloc[i]['rate']


select_model = ''
# two model comparison
avg1 = 0
avg2 = 0

n = len(model1)
for i in range(n):
    avg1 += dic[model1[i]]
    avg2 += dic[model2[i]]

avg1 = avg1 / n
avg2 = avg2 / n


if avg1 > avg2:
    select_model = 'ModelA'
else:
    select_model = 'ModelB'

print('Avg1  ' + str(avg1))
print('Avg2  ' + str(avg2))
print(select_model)










