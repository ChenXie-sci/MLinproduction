import os
import argparse
import numpy as np
import pandas as pd

##Curate Validation Data:

    #1) Data drift - newer patterns in data. 
    #2) Out of distributions - detect out of distribution data.
    #3) Check the most probable occuring movies. (Regression Testing)
    #4) Check users with different genres - subpopulations of them. 
    #5) New user id
    #

class ValidationData:

    def __init__(self,data):
        self.data = data
        self.val = pd.DataFrame(columns = ['Date', 'Number', 'Movie', 'moviename', 'rate'])
        
    
    def data_preprocess(self):
        #self.data[['name', 't']] = self.data['moviename'].str.split("=", n = 1, expand = True)
        self.data.drop(columns = ['Unnamed: 0'], inplace = True)


    def data_drift(self):
        ##We will here add more rarely top rated movies by some distinct users.
        ##Randomly select 50 rarely watched movies based on value counts of the movies
        indices = np.random.randint(-100,0,50)
        leastmovie = self.data['moviename'].value_counts()[indices].index.tolist()
        for movie in leastmovie:
            ind = self.data[self.data['moviename'] == movie]#[:5]#.tolist()[-5:]
            self.val = pd.concat([self.val , ind])#self.data.iloc[ind]])

        assert len(self.val) > 0 

        return self.val
        
    def low_distributed_data(self):
        ##We will here add most low rated movies of top rated users. 
        #First select the top rated users. From which select the lowest rated movies. 
        inilen = len(self.val)
        users = self.data.groupby(['Number', 'rate']).count()
        topusers = users.sort_values(by =['moviename'] , ascending = False)
        #print(topusers.index[:3])
        for ind in topusers.index[:200]:
            dat = self.data[(self.data['Number'] == ind[0])& (self.data['rate'] < 2)]
            if len(dat) >= 1:
                self.val = pd.concat([self.val , dat])
        assert len(self.val) > inilen

        return self.val

    def regression_testing(self):
        ##We will the most commonly rate movies that are common among the most number of users
        indices = np.random.randint(0,100,50)
        topmovie = self.data['moviename'].value_counts()[indices].index.tolist()
        inilen = len(self.val)
        for movie in topmovie:
            ind = self.data[self.data['moviename'] == movie]#[:5]#.tolist()[-5:]
            self.val = pd.concat([self.val , ind[:5]])#self.data.iloc[ind]])
            #print(ind[:5])
            #break
        #print(self.val.head())
        assert len(self.val) > inilen

        return self.val

    def subpopulation_data(self):
        ##We will make subpopulation based on the era in which the movies were released. 
        #We can have examples from movies from 1950s, 1990s, and 2000s
        t1950 = self.data[(self.data['year'] > 1950) & (self.data['year'] < 1955)]
        t1990 = self.data[(self.data['year'] > 1990) & (self.data['year'] < 1995)]
        t2000 = self.data[(self.data['year'] > 2000) & (self.data['year'] < 2005)]

        self.val = pd.concat([self.val. t1950[:5]]) 
        self.val = pd.concat([self.val. t1990[:5]]) 
        self.val = pd.concat([self.val. t2000[:5]]) 
        return self.val
        

    def filter_rows_by_values(self, df, values):
        return df[~df['Number'].isin(values)]

    def traindata_curation(self):
        ##Remove the UniqueIDs from 
        self.traindata = self.data
        valids = self.val['Number'].tolist()
        #for id in valids:
        self.traindata = self.filter_rows_by_values(self.traindata, valids)
        
        return self.traindata
        


#print(df.head())
#print((df['name'].value_counts()[-10:].index.tolist()))
#print(df['name'].value_counts()[-10:].index.tolist())