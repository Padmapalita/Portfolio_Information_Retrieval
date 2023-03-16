import numpy as np
import pandas as pd
import pickle

def BM25_IDF_df(df):
  """
  This definition calculates BM25-IDF weights before hand as done last week
  """
  print(len(df),'files in the BOW_index')
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


def create_BM25():
  """
  when called, manages the processing of the BOW_index.pickel
  and creates a BM25 index, saving it to pickel file stored in /Files
  """
  bag_of_words_DF = pd.read_pickle("../../Files/BOW_index.pkl")  
  

  print(len(bag_of_words_DF),'files in the BOW_index')
  dfs = (bag_of_words_DF > 0).sum(axis=0)
  N = bag_of_words_DF.shape[0]
  idfs = -np.log(dfs / N)
  
  k_1 = 1.2
  b = 0.8
  dls = bag_of_words_DF.sum(axis=1) 
  avgdl = np.mean(dls)

  numerator = np.array((k_1 + 1) * bag_of_words_DF)
  denominator = np.array(k_1 *((1 - b) + b * (dls / avgdl))).reshape(N,1) \
                         + np.array(bag_of_words_DF)

  BM25_tf = numerator / denominator

  idfs = np.array(idfs)

  BM25_score = BM25_tf * idfs
  bm25_df = pd.DataFrame(BM25_score, columns=bag_of_words_DF.columns)
  
  bm25_df.index = bag_of_words_DF.index
  #print(bm25_df[:5])
  bm25_df.to_pickle("../../Files/BM25_index.pkl")  
  #print("index has been created and pickled")
  return True

create_BM25()