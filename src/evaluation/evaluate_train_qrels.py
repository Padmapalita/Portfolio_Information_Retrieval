import numpy as np
import pandas as pd
import pickle

# import sys
# sys.path.append('../')
from search import Search 

class Evaluate:
    def __init__(self, k):
        #self.bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl") 
         
        print("initializing evaluate class")
        self.test_qrels_filename = "../../Files/2020_test_qrels.list.txt"
        self.train_filename = '../../Files/podcasts_2020_topics_train.xml'
        self.train_qrels_filename = "../../Files/2020_train_qrels.list.txt"
        self.test_filename = '../../Files/podcasts_2020_topics_test.xml'
        self.searcher = Search()
        self.k = k

    def get_train_qrels(self):
    # read the file from TrEC that contains the relevance scores
        with open(self.train_qrels_filename) as f:
            contents = f.read()
        # shorten the episode ID and split the time segment into seperate field
        lines = contents.replace('spotify:episode:','').replace('_','\t').replace(' ','\t').split("\n")
        data = [line.split('\t') for line in lines]
        # create dataframe and remove the second column which seems to have no value
        df = pd.DataFrame(data,columns = ['query_id', 'useless','episode','segment','relevance'])
        df = df.drop('useless', axis=1)
        # to resolve that final row has 'None' entries
        #df = df.drop(index=9426, axis=0)
        df['relevance'] = df['relevance'].astype(int)
        # the relevance scores are on scale 0-4, instead consider if it is relevant or not
        df['binary'] = df['relevance'] > 0
        df['binary'] = df['binary'].astype(int)
        # adjust query_id to start from 0
        df['query_id'] = df['query_id'].astype(int)
        # chage to -9 for test qrels
        df['query_id'] = df['query_id']-1 
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
    

    def get_queries(self):
    # read the file from TrEC that contains the query titles
        with open(self.train_filename) as f:
            contents = f.read()
        lines = contents.replace('<query>','\t').replace('</query>','\t').replace('</description>','\t').replace('<description>','\t').split("\t")
        data = [line.split('\t') for line in lines]
        y = data[1::2]
        query_list = y[0::2]
        #print(query_list)
        desc_list  = y[1::2]
        #print(desc_list)
        full_list = []
        for i in range(len(desc_list)):
            temp_list = ' '.join(query_list[i]) + ' ' + ' '.join(desc_list[i])
            full_list.append(temp_list)
        # put the queries into a dictionary but need to start numbering at 1
        self.queries = {i: val for i, val in enumerate(full_list)}
        return self.queries
    
    def confusion_matrix_at_k(self, query_id):
        """This function calculates the confusion matrix for k top ranking documents."""
        # function does not calculate TN as not relevant in the calculations
        doc_ranking = self.searcher.retrieve_ranking(self.queries[query_id])
        self.qrels = self.get_train_qrels()      

        # take only the document id, rather than the score
        retrieved = [doc[0] for doc in doc_ranking[:self.k]]
        #print(retrieved)
        #print(self.qrels)
        retrieved_relevant = [ep_ID for ep_ID in retrieved if [query_id, ep_ID, 1] in self.qrels]
        #print(len(retrieved_relevant))
        #print(retrieved_relevant)
        qrels_query = [qrel for qrel in self.qrels if qrel[0] == query_id]
        relevant_docs = [qrel[1] for qrel in qrels_query if qrel[-1] == 1]

        TP = len(retrieved_relevant)  # number of true positives
        FP = self.k - TP  # number of false positives
        FN = len(relevant_docs) - TP + 0.0001

        return TP, FP, FN
        
    def precision_at_k(self, query_id):
        TP, FP, FN = self.confusion_matrix_at_k(query_id)
        precision = TP / self.k
        return precision
    
    def print_precision_for_all_queries(self,):
        self.queries = self.get_queries()
        for query_id, query in self.queries.items():
            TP, FP, FN = self.confusion_matrix_at_k(query_id)
            precision = self.precision_at_k(query_id) 
            print(f'retrieved query "{query}" with precision @ {self.k}: {precision} (TP: {TP}, FP: {FP})')

    def recall_at_k(self, query_id):
        TP, FP, FN = self.confusion_matrix_at_k(query_id)
        recall = TP / (TP+FN)
        return recall

    def print_recall_for_all_queries(self,):
        self.queries = self.get_queries()
        for query_id, query in self.queries.items():
            TP, FP, FN = self.confusion_matrix_at_k(query_id)
            recall = self.recall_at_k(query_id) 
            print(f'retrieved query "{query}" with recall @ {self.k}: {recall} (TP: {TP}, FN: {FN})')


    def evaluate(self, ):
        self.print_precision_for_all_queries()
        self.print_recall_for_all_queries()
        return 

evaulate = Evaluate(k = 10)
evaulate.evaluate()