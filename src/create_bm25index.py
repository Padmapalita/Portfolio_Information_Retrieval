import numpy as np
import pandas as pd
import pickle

def BM25_IDF_df(df):
  """
  This definition calculates BM25-IDF weights before hand as done last week
  """

  dfs = (df > 0).sum(axis=0)
  N = df.shape[0]
  idfs = -np.log(dfs / N)
  
  k_1 = 1.2
  b = 0.8
  dls = df.sum(axis=1) 
  avgdl = np.mean(dls)

  numerator = np.array((k_1 + 1) * df)
  denominator = np.array(k_1 *((1 - b) + b * (dls / avgdl))).reshape(N,1) \
                         + np.array(df)

  BM25_tf = numerator / denominator

  idfs = np.array(idfs)

  BM25_score = BM25_tf * idfs
  return pd.DataFrame(BM25_score, columns=df.columns)

bag_of_words_DF = pd.read_pickle("../Files/BOW_index.pkl")  


bm25_df = BM25_IDF_df(bag_of_words_DF)
bm25_df.index = bag_of_words_DF.index

print(bm25_df[:5])
bm25_df.to_pickle("../Files/BM25_index.pkl")  
print("index has been created and pickled")