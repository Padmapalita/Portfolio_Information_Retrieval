import numpy as np
import pandas as pd

class Search:
    def __init__(self, mode='default'):
        print("from Search trying to load pickle \n")
        if mode == 'testing': # hidden option for testing
            self.bm25_df = pd.read_pickle("../Files/Local_pickles/testing_index.pkl")
        else:
            print("Enter the filename of the pickle to load (including the '.pkl' extension),")
            filename = input("or [D] to use the default option: ")
            if filename == 'D':
                #self.bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_v909_k215_b09.pkl")
                self.bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_v905_k20_b09.pkl")
                #self.bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_Final_k20_b09.pkl")
                
            else:
                filename = "../Files/Local_pickles/" + filename
                self.bm25_df = pd.read_pickle(filename)
    
        print("un-pickled \n")


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
        sorted_scores = [score_pair for score_pair in sorted_scores
                         if score_pair[1] > 0]
        return sorted_scores
    
    def retrieve_with_expansion(self, query ):
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
        # get 5 most common words from top 3 ranked documents
        for i in range(3):
            new_words.extend(self.bm25_df.loc[sorted_scores[i][0]].nlargest(5).index.tolist())
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
        sorted_scores = [score_pair for score_pair in sorted_scores
                         if score_pair[1] > 0]
        return sorted_scores
    
    def lookup_metadata(self, list):
        """
        This version should return human readable results 
        """
        # Assumes will never want more than 100 results
        metadata = pd.read_csv("../Files/Local_pickles/metadata.csv", index_col="episode_filename_prefix")
        # metadata = pd.read_csv("../Files/Local_pickles/metadata_test.csv", index_col="episode_filename_prefix")
        print("csv has been read")
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
                "Episode description" : result_line.loc["episode_description"]
                }
             )
        return readable_result


# test = Search()
# list = [
#     ("0ixFmXbhwF8qNK9i4QLbQv", 0.5),
#     ("0iyJ0bKe31H0p9PN5u3xmG", 0.4)
# ]
# print(test.lookup_metadata(list))