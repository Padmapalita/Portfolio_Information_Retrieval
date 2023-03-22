import numpy as np
import pandas as pd
import pickle

class Search:
    def __init__(self,):
        print("from Search trying to load pickle")
        self.bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_in_one_index.pkl")  
        print("un-pickled")


    def retrieve_ranking(self, query ):
        """
        returns the BM25 results as a list of tuples (df.index,value, BM25_score)
        """
        q_terms = query.split(' ')
        q_terms_only = self.bm25_df[q_terms]
        score_q_d = q_terms_only.sum(axis=1)
        return sorted(zip(self.bm25_df.index.values, score_q_d.values),
                        key = lambda tup:tup[1],
                        reverse=True)
    
    def lookup_titles(list):
        """
        This version should return human readable results 
        """
        ### TODO: Need to have the retrieve ranking return index.values AND episode information
        # return human_readable 

