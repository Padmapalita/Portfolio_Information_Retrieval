import numpy as np

N = 2
dls = [7, 11]
dfs = {'actually' : 1, 'cheese' : 1, 'come' : 1, 'episode' : 1, 'football' : 1, 'hi' : 1,
        'misleading' : 1, 'podcast' : 2, 'podcasts' : 1, 'probably' : 1, 'promising' : 1,
        'round' : 1, 'talking' : 1, 'today' : 1, 'welcome' : 1}
tfs = [[0, 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 0, 1, 1, 1],
                [1, 1, 1, 1, 2, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0]]
k = 1.2
b = 0.8
avdl = np.mean(dls)
# idf = - np.log(tfs / N)
# numerator = (k+1) * tfs
# denominator = k * ((1-b) + b*dl/avdl) + tf
# BM25_score = numerator / denominator * idf
# BM25_score

tf = 1
dl = dls[1]
idf = - np.log(tf / N)
numerator = (k+1) * tf
denominator = k * ((1-b) + b*dl/avdl) + tf
print(numerator / denominator * idf)