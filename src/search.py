import numpy as np
import pandas as pd
import pickle

class Search:
    def __init__(self,):
        #self.bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl")  
        print("un-pickled")

    def return_bm25_index():
        bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl")  
        return bm25_df

    def retrieve_ranking(self, query, bm25_df ):
        q_terms = query.split(' ')
        q_terms_only = bm25_df[q_terms]
        score_q_d = q_terms_only.sum(axis=1)
        return sorted(zip(bm25_df.index.values, score_q_d.values),
                        key = lambda tup:tup[1],
                        reverse=True)

