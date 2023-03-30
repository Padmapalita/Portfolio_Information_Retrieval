import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle

# import sys
# sys.path.append('../')
# from search import Search
from search import Search 

class Evaluate:
    def __init__(self, k):
        #self.bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl") 
         
        print("initializing evaluate class")
        # self.test_qrels_filename = "../../Files/2020_test_qrels.list.txt"
        # self.train_filename = '../../Files/podcasts_2020_topics_train.xml'
        # self.train_qrels_filename = "../../Files/2020_train_qrels.list.txt"
        # self.test_filename = '../../Files/podcasts_2020_topics_test.xml'
        self.test_qrels_filename = "../Files/2020_test_qrels.list.txt"
        self.train_filename = '../Files/podcasts_2020_topics_train.xml'
        self.train_qrels_filename = "../Files/2020_train_qrels.list.txt"
        self.test_filename = '../Files/podcasts_2020_topics_test.xml'
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
            temp_list = ' '.join(query_list[i]).lower() + ' ' + ' '.join(desc_list[i]).lower()
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

        # list, 1 when kth item is relevant, or 0 when it is not
        rels = [int(x in retrieved_relevant) for x in retrieved]

        TP = len(retrieved_relevant)  # number of true positives
        FP = self.k - TP  # number of false positives
        if len(relevant_docs) == len(retrieved_relevant):
            FN = 0
        else:
            FN = len(relevant_docs) - TP

        return TP, FP, FN, rels
        
    def precision_at_k(self, query_id):
        TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
        precision = TP / self.k
        return precision
    
    def print_precision_for_all_queries(self,):
        self.queries = self.get_queries()
        for query_id, query in self.queries.items():
            TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
            precision = self.precision_at_k(query_id) 
            print(f'retrieved query "{query}" with precision @ {self.k}: {precision} (TP: {TP}, FP: {FP})')

    def recall_at_k(self, query_id):
        TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
        recall = TP / (TP+FN)
        return recall

    def print_recall_for_all_queries(self,):
        self.queries = self.get_queries()
        for query_id, query in self.queries.items():
            TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
            recall = self.recall_at_k(query_id) 
            print(f'retrieved query "{query}" with recall @ {self.k}: {recall} (TP: {TP}, FN: {FN})')


    def plot_precision_recall_pairs(self):
        self.queries = self.get_queries()

        all_query_precisions = []
        all_query_recalls = []
        all_query_rels = []

        # loop to get precision and recall into big lists
        for query_id, query in self.queries.items():
            TP,FP,FN, rels = self.confusion_matrix_at_k(query_id)
            all_query_rels.append(rels)

            fake_k = self.k
            for i in range(fake_k):
                self.k = i + 1
                all_query_precisions.append(self.precision_at_k(query_id))
                all_query_recalls.append(self.recall_at_k(query_id))
            self.k = fake_k
        all_query_rels = np.array(all_query_rels).flatten().tolist()
        
        # calculate average precision and recall across all ks and all queries
        overall_average_precision = sum(all_query_precisions)/len(all_query_precisions)
        overall_average_recall = sum(all_query_recalls)/len(all_query_recalls)
        print(f'Overall average precision: {overall_average_precision}')
        print(f'Overall average recall: {overall_average_recall}')

        # create a dataframe of precision recall pairs by slicing the lists at each kth element
        df_all_queries = pd.DataFrame()
        all_APs = []
        for i in range (len(self.queries)):
            df_all_queries[f'query{i+1}_precision'] = all_query_precisions[i*self.k : self.k*i+self.k]
            df_all_queries[f'query{i+1}_recall'] = all_query_recalls[i*self.k : self.k*i+self.k]
            x = all_query_rels[i*self.k : self.k*i+self.k]
            y = all_query_precisions[i*self.k : self.k*i+self.k]
            AP = (np.multiply(x,y).sum())/sum(y)
            all_APs.append(AP)
            #print(all_query_precisions[i*self.k : self.k*i+self.k])
        
        # select odd columns to calculate mean precision
        df_all_queries['Avg_precision_across_queries'] = df_all_queries.iloc[:, 0::2].mean(axis=1)
        # select even columns to calculate mean recall
        df_all_queries['Average_recall_across_queries'] = df_all_queries.iloc[:, 1::2].mean(axis=1)
        df_all_queries.to_csv("../Files/sample.csv", index = True)

        # caluclate overall Mean Averge Precision metric
        mean_AP= sum(all_APs)/len(all_APs)
        print(f'the mean average precision for all queries is {round(mean_AP,3)}') 

        # create individual precision-recall plots for each query
        for i in range (len(self.queries)):
            df_all_queries.plot(x=f'query{i+1}_recall', y = f'query{i+1}_precision', kind = 'line', legend=False)
            plt.xlabel(f'Query {i+1} Recall')
            plt.ylabel(f'Query {i+1} Precision')
            plt.title(f'Query {i+1} Precision-Recall Pairs')
            plt.savefig(f"../Files/precision_recall_query{i+1}.png", dpi=300)

        # create average across all queries precision-recall plot
        df_all_queries.plot(x='Average_recall_across_queries', y='Avg_precision_across_queries',  kind = 'line', legend=False)
        plt.xlabel('Average recall')
        plt.ylabel('Average precision')
        plt.title('Average Precision-Recall Pairs across all queriess')
        plt.savefig("../Files/average_precision_recall_all_queries.png", dpi=300)
        return df_all_queries

    def evaluate(self, ):
        #self.print_precision_for_all_queries()
        #self.print_recall_for_all_queries()
        self.plot_precision_recall_pairs()
        return 

evaulate = Evaluate(k = 30)
evaulate.evaluate()
