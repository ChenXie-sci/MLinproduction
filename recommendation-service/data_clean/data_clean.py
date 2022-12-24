import pandas as pd 


def data_streaming(file):
    data = pd.read_csv(file ,usecols=[2])
    # remove duplicate data
    data = data.drop_duplicates()


    df = pd.DataFrame()

    n = len(data)
    for i in range(n):
        array = data.iloc[i].to_string().split(' ')
        movie = array[6]
        try:
            if 0 <= int(movie[-1]) <= 5:
                if movie.islower():
                    df = df.append(data.iloc[i])
        except:
            continue

    df.to_csv("clean_rate.txt", header=None, index=None, sep=',', mode='w')
    return df

# file = 'rate.txt'

# data_streaming(file)






