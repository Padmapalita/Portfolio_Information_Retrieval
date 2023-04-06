import numpy as np
import pandas as pd
import pickle

class AppSearch:
    def __init__(self,):
        print("Loading the BM25 pickle")
        print("loading may take around 20 seconds")
        self.bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_Final_k20_b09.pkl")  
        print("Searching")


    def retrieve_ranking(self, query ):
        """
        returns the BM25 results as a list of tuples (df.index,value, BM25_score)
        """
        q_terms = query.split(' ')
        # Only counts query terms that are in the bm25_df, to avoid KeyError
        q_terms = [term for term in q_terms if term in self.bm25_df.columns]
        q_terms_only = self.bm25_df[q_terms]
        score_q_d = q_terms_only.sum(axis=1)
        sorted_scores = sorted(zip(self.bm25_df.index.values, score_q_d.values),
                        key = lambda tup:tup[1],
                        reverse=True)
        return sorted_scores
    
    def retrieve_with_query_expansion(self, query ):
        # this includes two hyperparameters that could be tuned
        """
        returns the BM25 results as a list of tuples (df.index,value, BM25_score)
        """
        q_terms = query.split(' ')
        # Only counts query terms that are in the bm25_df, to avoid KeyError
        q_terms = [term for term in q_terms if term in self.bm25_df.columns]
        q_terms_only = self.bm25_df[q_terms]
        score_q_d = q_terms_only.sum(axis=1)
        sorted_scores = sorted(zip(self.bm25_df.index.values, score_q_d.values),
                        key = lambda tup:tup[1],
                        reverse=True)
        
        # pseudo relevance feedback - using information derived from initial ranking to expand query 
        new_words = []
        # get the top 3 documents from ranking
        for i in range(3):
            idf = bm25_df.sort_values(by = [sort[i][0]], axis = 1, ascending = False)
            # find the 5 most common words
            new_words.extend(idf.columns.values[:5].tolist())
        new_words = ' '.join(new_words)
        query = query + ' ' + new_words 
        
        # re-run the ranking
        q_terms = query.split(' ')
        q_terms = [term for term in q_terms if term in self.bm25_df.columns]
        q_terms_only = self.bm25_df[q_terms]
        score_q_d = q_terms_only.sum(axis=1)
        sorted_scores = sorted(zip(self.bm25_df.index.values, score_q_d.values),
                        key = lambda tup:tup[1],
                        reverse=True)
        return sorted_scores
    
    def lookup_metadata(self, list):
        """
        This version should return human readable results 
        """
        # Assumes will never want more than 100 results
        metadata = pd.read_csv("../Files/Local_pickles/metadata.csv", index_col="episode_filename_prefix")
        #print("csv has been read")
        #print(metadata[:5])
        readable_result = []
        for i, result in enumerate(list[:100]):
            result_line = metadata.loc[result[0]]
            readable_result.append(
                {
                f"Search result {i+1}" : round(result[1], 2),
                "Show name" : result_line.loc["show_name"],
                "Episode title" : result_line.loc["episode_name"],
                "Episode duration (minutes)" : round(result_line.loc["duration"], 2),
                "Show description" : result_line.loc["show_description"],
                "Episode description" : result_line.loc["episode_description"],
                "rss_link" : result_line.loc["rss_link"]
                }
             )
        return readable_result


# test = Search()
# list = [
#     ("0ixFmXbhwF8qNK9i4QLbQv", 0.5),
#     ("0iyJ0bKe31H0p9PN5u3xmG", 0.4)
# ]
# print(test.lookup_metadata(list))
