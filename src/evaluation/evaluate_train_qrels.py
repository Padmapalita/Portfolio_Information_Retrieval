import os
os.system('pip install beautifulsoup4')
from beautifulsoup4 import BeautifulSoup
import numpy as np
import pandas as pd
import pickle

# import sys
# sys.path.append('../')
from search import Search 

class Evaluate:
    def __init__(self,):
        print("trying to load pickle")
        #self.bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl") 
         
        print("un-pickled")
        self.train_qrels_filename = "../../Files/2020_test_qrels.list.txt"
        self.train_filename = '../../Files/podcasts_2020_topics_train.xml'
        self.searcher = Search()

    def get_test_qrels(self, filename):
    # read the file from TrEC that contains the relevance scores
        with open(filename) as f:
            contents = f.read()
        # shorten the episode ID and split the time segment into seperate field
        lines = contents.replace('spotify:episode:','').replace('_','\t').replace(' ','\t').split("\n")
        data = [line.split('\t') for line in lines]
        # create dataframe and remove the second column which seems to have no value
        df = pd.DataFrame(data,columns = ['query_id', 'useless','episode','segment','relevance'])
        df = df.drop('useless', axis=1)
        # to resolve that final row has 'None' entries
        df = df.drop(index=9426, axis=0)
        df['relevance'] = df['relevance'].astype(int)
        # the relevance scores are on scale 0-4, instead consider if it is relevant or not
        df['binary'] = df['relevance'] > 0
        df['binary'] = df['binary'].astype(int)
        # adjust query_id to start from 0
        df['query_id'] = df['query_id'].astype(int)
        df['query_id'] = df['query_id']-9
        # if an episode has relevance at 'some' point then consider the whole episode to be relevant
        df2 = df.groupby(['episode','query_id'])['binary'].max()
        # adjusting the datagrame into a list with (query_id, document_id, judgement)
        cols = ['query_id', 'episode', 'binary']
        df2 = df2.reset_index()
        df2['query_id'] = df2['query_id'].astype(int)
        self.qrels = df2[cols].values.tolist()
        return self.qrels
    # test_qrels = get_test_qrels("Files/2020_test_qrels.list.txt")
    # test_qrels[:5]
    

    def get_queries(self, filename):
    # read the file from TrEC that contains the query titles
        with open(filename) as f:
            contents = f.read()
        
        soup = BeautifulSoup(contents, 'xml')
        desc_list = [desc.text for desc in soup.find_all('description')]
        query_list = [query.text for query in soup.find_all('query')]
        full_list = []
        for i in range(len(desc_list)):
            temp_list = query_list[i] + ' ' + desc_list[i]
            full_list.append(temp_list)
        # put the queries into a dictionary but need to start numbering at 1
        self.queries = {i: val for i, val in enumerate(full_list)}
        return self.queries
    

        
    def precision_at_k(self, query_id, k):
        """This function considers the k top ranking documents."""
        doc_ranking = self.searcher.retrieve_ranking(self.queries[query_id], self.bm25_df)
        self.qrels = self.get_test_qrels(self.train_qrels_filename)

        # take only the document id, rather than the score
        retrieved = [doc[0] for doc in doc_ranking[:k]]
        print(retrieved)
        retrieved_relevant = [ep_ID for ep_ID in retrieved if [query_id, ep_ID, 1] in self.qrels]
        
        print(retrieved_relevant)
        TP = len(retrieved_relevant)  # number of true positives
        FP = k - TP  # number of false positives
        precision = TP / k

        return TP, FP, precision
    
    def print_precision_for_all_queries(self,):
        k=3
        self.queries = self.get_queries(self.train_qrels_filename)
        for query_id, query in self.queries.items():
            TP, FP, precision = self.precision_at_k(query_id, k=k) 
            print(f'retrieved query "{query}" with precision @ {k}: {precision} (TP: {TP}, FP: {FP})')

       

    def evaluate(self, ):
        
        self.print_precision_for_all_queries()
        return 

evaulate = Evaluate()
evaulate.evaluate()