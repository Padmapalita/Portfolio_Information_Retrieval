import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pickle
import nltk 
nltk.download('wordnet')
nltk.download('omw-1.4')
from nltk.corpus import wordnet

# import sys
# sys.path.append('../')
from search import Search 

class Evaluate:
    def __init__(self, inc_desc=True, use_synonym=False, mode='default', train_test='train', expansion=False):
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
        self.searcher = Search(mode=mode)
        self.k = 100
        self.inc_desc = inc_desc
        self.use_synonym = use_synonym
        self.version = "desc_false_k20_b09"
        self.train_test = train_test
        self.expansion = expansion

    def get_qrels(self):
    # read the file from TrEC that contains the relevance scores
        if self.train_test == 'train':
            filename = self.train_qrels_filename
        elif self.train_test == 'test':
            filename = self.test_qrels_filename
        with open(filename) as f:
            contents = f.read()
        # shorten the episode ID and split the time segment into seperate field
        lines = contents.replace('spotify:episode:','').replace('_','\t').replace(' ','\t').split("\n")
        data = [line.split('\t') for line in lines]
        # create dataframe and remove the second column which seems to have no value
        df = pd.DataFrame(data,columns = ['query_id', 'useless','episode','segment','relevance'])
        df = df.drop('useless', axis=1)
        
        if self.train_test == 'test':
            df = df.drop(index=9426, axis=0)
        
        df['relevance'] = df['relevance'].astype(int)
        # the relevance scores are on scale 0-4, instead consider if it is relevant or not
        df['binary'] = df['relevance'] > 0
        df['binary'] = df['binary'].astype(int)
        # adjust query_id to start from 0
        df['query_id'] = df['query_id'].astype(int)
        
        if self.train_test == 'train':
            adjustment = 1
        elif self.train_test == 'test':
            adjustment = 9
        df['query_id'] = df['query_id']-adjustment
        # if an episode has relevance at 'some' point then consider the whole episode to be relevant
        df2 = df.groupby(['episode','query_id'])['binary'].max()
        # adjust the datagrame into a list with (query_id, document_id, judgement)
        cols = ['query_id', 'episode', 'binary']
        df2 = df2.reset_index()
        df2['query_id'] = df2['query_id'].astype(int)
        self.qrels = df2[cols].values.tolist()
        return self.qrels

    def get_queries(self):
    # read the file from TrEC that contains the query titles
        if self.train_test == 'train':
            filename = self.train_filename
        elif self.train_test == 'test':
            filename = self.test_filename
        with open(filename) as f:
            contents = f.read()
        # isolate 'query' and 'description' fields with tabs
        lines = contents.replace('<query>','\t').replace('</query>','\t').replace('</description>','\t').replace('<description>','\t').split("\t")
        # seperate 'query' and 'description' onto seperate lines
        data = [line.split('\t') for line in lines]
        # filter for query
        y = data[1::2]
        query_list = y[0::2]
        
        # this is a query use_synonym expansion, it takes the short query and adds synonyms to it
        if self.use_synonym:
            temp_query_list = []
            for i in range(len(query_list)):
                synonyms = []
                q = ' '.join(query_list[i])
                # split query into seperate terms
                q_terms = q.split(' ')
                for x in q_terms:
                    # this ensures that if no synonyms the term is still added back
                    if len(wordnet.synsets(x)) == 0:
                        synonyms.append(x)
                    else:
                        # this find the definitions for a term
                        for syn in wordnet.synsets(x):
                            # this find the synonyms for a definition
                            for term in syn.lemmas():
                                synonyms.append(term.name())
                temp_query_list.append(synonyms)
            query_list=temp_query_list

        # creates a list of empty lists that will be overwritten if inc_desc=True
        desc_list = [[] for x in range(len(query_list))]
            # this will include the lengthier 'description' within query
        if self.inc_desc:
            # filter for description
            desc_list  = y[1::2]
        full_list = []
        for i in range(len(desc_list)):
            temp_list = ' '.join(query_list[i]).lower() + ' ' + ' '.join(desc_list[i]).lower()
            full_list.append(temp_list)
        # put the queries into a dictionary
        
        self.queries = {i: val for i, val in enumerate(full_list)}
        
        print("queries retreived")
        
        return self.queries
    
    def confusion_matrix_at_k(self, query_id):
        """This function calculates the confusion matrix for k top ranking documents."""
        self.k = 100
        # function does not calculate TN as not relevant in the calculations
        doc_ranking = self.searcher.retrieve_ranking(self.queries[query_id])
        # this is expansion via 5 most frequency occuring words in the top three docs
        # if self.expansion == False:
        #     doc_ranking = self.searcher.retrieve_ranking(self.queries[query_id])
        # elif self.expansion == True:
        #     doc_ranking = self.searcher.retrieve_with_expansion(self.queries[query_id])
        self.qrels = self.get_qrels()
        if len(doc_ranking) < self.k:
            new_k = len(doc_ranking)
            print(f"Only {new_k} documents retrieved out of intended {self.k}.")
            #self.k = new_k
            #doc_ranking = doc_ranking[:self.k]

        # document IDs of retrieved documents
        retrieved = [doc[0] for doc in doc_ranking[:self.k]]
        # document IDs of retrieved relevant documents
        retrieved_relevant = [ep_ID for ep_ID in retrieved if [query_id, ep_ID, 1] in self.qrels]
        # qrels for specific query
        qrels_query = [qrel for qrel in self.qrels if qrel[0] == query_id]
        # relevant docs for specific query
        relevant_docs = [qrel[1] for qrel in qrels_query if qrel[-1] == 1]

        # 1 when kth retrieved document is relevant, 0 when not
        rels = [int(x in retrieved_relevant) for x in retrieved]

        TP = len(retrieved_relevant)  # number of true positives
        FP = self.k - TP  # number of false positives
        if len(relevant_docs) == len(retrieved_relevant):
            FN = 0
        else:
            FN = len(relevant_docs) - TP # number of false negatives
        print("True Postives calculated")
        return TP, FP, FN, rels
        
    def precision_at_k(self, query_id):
        TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
        precision = TP / self.k
        return precision
    
    # def print_precision_for_all_queries(self,):
    #     self.queries = self.get_queries()
    #     for query_id, query in self.queries.items():
    #         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
    #         precision = self.precision_at_k(query_id) 
    #         print(f'retrieved query "{query}" with precision @ {self.k}: {precision} (TP: {TP}, FP: {FP})')

    def recall_at_k(self, query_id):
        TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
        recall = 0
        if TP + FN != 0 :
            recall = TP / (TP+FN)
       
        return recall

    # def print_recall_for_all_queries(self,):
    #     self.queries = self.get_queries()
    #     for query_id, query in self.queries.items():
    #         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
    #         recall = self.recall_at_k(query_id) 
    #         print(f'retrieved query "{query}" with recall @ {self.k}: {recall} (TP: {TP}, FN: {FN})')


    def plot_precision_recall_pairs(self):
       
        self.queries = self.get_queries()

        all_query_precisions = []
        all_query_recalls = []
        all_query_rels = []

        # loop to get precision and recall into big lists
        for query_id, query in self.queries.items():
            
            print("processing query: ", query)
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
        # overall_average_precision = sum(all_query_precisions)/len(all_query_precisions)
        # overall_average_recall = sum(all_query_recalls)/len(all_query_recalls)
        # print(f'Overall average precision: {overall_average_precision}')
        # print(f'Overall average recall: {overall_average_recall}')

        # create a dataframe of precision recall pairs by slicing the lists at each kth element
        #df_all_queries = pd.DataFrame()
        
        all_APs = []
        for i in range (len(self.queries)):
            print("started plotting query ", i+1)
            # for each query get a list of precision, recall and rel (0/1) values at every k
            p = all_query_precisions[i*self.k : self.k*i+self.k]
            r = all_query_recalls[i*self.k : self.k*i+self.k]
            x = all_query_rels[i*self.k : self.k*i+self.k]
            # product of precision/recall with rel in order to zero out values when non-relevant doc retrieved
            px = np.multiply(p,x)
            rx = np.multiply(r,x)
            
            # put list of non-zero precision/recall values into df
            precision_list = [a for a in px if a>0]
            recall_list = [a for a in rx if a>0]

            plt.plot(recall_list, precision_list, label=f"query {i+1}")
            plt.xlabel(f'Query {i+1} Recall')
            plt.ylabel(f'Query {i+1} Precision')
            plt.xlim([0,1])
            plt.ylim([0,1])
            plt.title(f'Query {i+1} Precision-Recall Pairs')

            plt.savefig(f"../Files/Local_pickles/precision_recall_query{i+1}{self.version}.png", dpi=300)
            plt.show()

            print("finished plotting query ", i+1)
            # average precision calculation
            AP = px.sum()/sum(x)
            all_APs.append(AP)
            continue
        
        #df_all_queries.to_csv("../Files/sample.csv", index = True)

        # caluclate overall Mean Averge Precision metric
        AP_df = pd.DataFrame(all_APs, columns=['precisions'])
        AP_df.to_csv('../Files/Local_pickles/AP_test_result.csv')
        all_APs = [AP for AP in all_APs if not np.isnan(AP)]
        mean_AP= sum(all_APs)/len(all_APs)
        print(f'the mean average precision for all queries is {round(mean_AP,3)}') 
        return

    def evaluate(self, ):
        self.plot_precision_recall_pairs()
        return 

# for experiments we will try inc_desc=False and use_synonym=True as parameters of Evaluate
evaulate = Evaluate(inc_desc=True ,use_synonym=False,expansion=False,  train_test='test')
evaulate.evaluate()


# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import pickle
# import nltk 
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# from nltk.corpus import wordnet

# # import sys
# # sys.path.append('../')
# from search import Search 

# class Evaluate:
#     def __init__(self, k, inc_desc=True, use_synonym=False, mode='default', train_test='train', expansion=False):
#         #self.bm25_df = pd.read_pickle("../../Files/Local_pickles/BM25_in_one_index.pkl") 
         
#         print("initializing evaluate class")
#         # self.test_qrels_filename = "../../Files/2020_test_qrels.list.txt"
#         # self.train_filename = '../../Files/podcasts_2020_topics_train.xml'
#         # self.train_qrels_filename = "../../Files/2020_train_qrels.list.txt"
#         # self.test_filename = '../../Files/podcasts_2020_topics_test.xml'
#         self.test_qrels_filename = "../Files/2020_test_qrels.list.txt"
#         self.train_filename = '../Files/podcasts_2020_topics_train.xml'
#         self.train_qrels_filename = "../Files/2020_train_qrels.list.txt"
#         self.test_filename = '../Files/podcasts_2020_topics_test.xml'
#         self.searcher = Search(mode=mode)
#         self.k = k
#         self.inc_desc = inc_desc
#         self.use_synonym = use_synonym
#         self.version = "demo_k20_b09"
#         self.train_test = train_test
#         self.expansion = expansion

#     def get_qrels(self):
#     # read the file from TrEC that contains the relevance scores
#         if self.train_test == 'train':
#             filename = self.train_qrels_filename
#         elif self.train_test == 'test':
#             filename = self.test_qrels_filename
#         with open(filename) as f:
#             contents = f.read()
#         # shorten the episode ID and split the time segment into seperate field
#         lines = contents.replace('spotify:episode:','').replace('_','\t').replace(' ','\t').split("\n")
#         data = [line.split('\t') for line in lines]
#         # create dataframe and remove the second column which seems to have no value
#         df = pd.DataFrame(data,columns = ['query_id', 'useless','episode','segment','relevance'])
#         df = df.drop('useless', axis=1)
        
#         if self.train_test == 'test':
#             df = df.drop(index=9426, axis=0)
        
#         df['relevance'] = df['relevance'].astype(int)
#         # the relevance scores are on scale 0-4, instead consider if it is relevant or not
#         df['binary'] = df['relevance'] > 0
#         df['binary'] = df['binary'].astype(int)
#         # adjust query_id to start from 0
#         df['query_id'] = df['query_id'].astype(int)
        
#         if self.train_test == 'train':
#             adjustment = 1
#         elif self.train_test == 'test':
#             adjustment = 9
#         df['query_id'] = df['query_id']-adjustment
#         # if an episode has relevance at 'some' point then consider the whole episode to be relevant
#         df2 = df.groupby(['episode','query_id'])['binary'].max()
#         # adjust the datagrame into a list with (query_id, document_id, judgement)
#         cols = ['query_id', 'episode', 'binary']
#         df2 = df2.reset_index()
#         df2['query_id'] = df2['query_id'].astype(int)
#         self.qrels = df2[cols].values.tolist()
#         return self.qrels

#     def get_queries(self):
#     # read the file from TrEC that contains the query titles
#         if self.train_test == 'train':
#             filename = self.train_filename
#         elif self.train_test == 'test':
#             filename = self.test_filename
#         with open(filename) as f:
#             contents = f.read()
#         # isolate 'query' and 'description' fields with tabs
#         lines = contents.replace('<query>','\t').replace('</query>','\t').replace('</description>','\t').replace('<description>','\t').split("\t")
#         # seperate 'query' and 'description' onto seperate lines
#         data = [line.split('\t') for line in lines]
#         # filter for query
#         y = data[1::2]
#         query_list = y[0::2]
        
#         # this is a query use_synonym expansion, it takes the short query and adds synonyms to it
#         if self.use_synonym:
#             temp_query_list = []
#             for i in range(len(query_list)):
#                 synonyms = []
#                 q = ' '.join(query_list[i])
#                 # split query into seperate terms
#                 q_terms = q.split(' ')
#                 for x in q_terms:
#                     # this ensures that if no synonyms the term is still added back
#                     if len(wordnet.synsets(x)) == 0:
#                         synonyms.append(x)
#                     else:
#                         # this find the definitions for a term
#                         for syn in wordnet.synsets(x):
#                             # this find the synonyms for a definition
#                             for term in syn.lemmas():
#                                 synonyms.append(term.name())
#                 temp_query_list.append(synonyms)
#             query_list=temp_query_list

#         # creates a list of empty lists that will be overwritten if inc_desc=True
#         desc_list = [[] for x in range(len(query_list))]
#             # this will include the lengthier 'description' within query
#         if self.inc_desc:
#             # filter for description
#             desc_list  = y[1::2]
#         full_list = []
#         for i in range(len(desc_list)):
#             temp_list = ' '.join(query_list[i]).lower() + ' ' + ' '.join(desc_list[i]).lower()
#             full_list.append(temp_list)
#         # put the queries into a dictionary
        
#         self.queries = {i: val for i, val in enumerate(full_list)}
        
#         print("queries retreived")
        
#         return self.queries
    
#     def confusion_matrix_at_k(self, query_id):
#         """This function calculates the confusion matrix for k top ranking documents."""
#         # function does not calculate TN as not relevant in the calculations
#         doc_ranking =[]
#         # this is expansion via 5 most frequency occuring words in the top three docs
#         if self.expansion == False:
#             doc_ranking = self.searcher.retrieve_ranking(self.queries[query_id])
#         elif self.expansion == True:
#             doc_ranking = self.searcher.retrieve_with_expansion(self.queries[query_id])
#         self.qrels = self.get_qrels()
#         if len(doc_ranking) < self.k:
#             new_k = len(doc_ranking)
#             print(f"Only {new_k} documents retrieved out of intended {self.k}.")
#             self.k = new_k

#         # document IDs of retrieved documents
#         retrieved = [doc[0] for doc in doc_ranking[:self.k]]
#         # document IDs of retrieved relevant documents
#         retrieved_relevant = [ep_ID for ep_ID in retrieved if [query_id, ep_ID, 1] in self.qrels]
#         # qrels for specific query
#         qrels_query = [qrel for qrel in self.qrels if qrel[0] == query_id]
#         # relevant docs for specific query
#         relevant_docs = [qrel[1] for qrel in qrels_query if qrel[-1] == 1]

#         # 1 when kth retrieved document is relevant, 0 when not
#         rels = [int(x in retrieved_relevant) for x in retrieved]

#         TP = len(retrieved_relevant)  # number of true positives
#         FP = self.k - TP  # number of false positives
#         if len(relevant_docs) == len(retrieved_relevant):
#             FN = 0
#         else:
#             FN = len(relevant_docs) - TP # number of false negatives
#         print("True Postives calculated")
#         return TP, FP, FN, rels
        
#     def precision_at_k(self, query_id):
#         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
#         precision = TP / self.k
#         return precision
    
#     # def print_precision_for_all_queries(self,):
#     #     self.queries = self.get_queries()
#     #     for query_id, query in self.queries.items():
#     #         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
#     #         precision = self.precision_at_k(query_id) 
#     #         print(f'retrieved query "{query}" with precision @ {self.k}: {precision} (TP: {TP}, FP: {FP})')

#     def recall_at_k(self, query_id):
#         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
#         recall = 0
#         if TP + FN != 0 :
#             recall = TP / (TP+FN)
       
#         return recall

#     # def print_recall_for_all_queries(self,):
#     #     self.queries = self.get_queries()
#     #     for query_id, query in self.queries.items():
#     #         TP, FP, FN, rels = self.confusion_matrix_at_k(query_id)
#     #         recall = self.recall_at_k(query_id) 
#     #         print(f'retrieved query "{query}" with recall @ {self.k}: {recall} (TP: {TP}, FN: {FN})')


#     def plot_precision_recall_pairs(self):
#         self.queries = self.get_queries()

#         all_query_precisions = []
#         all_query_recalls = []
#         all_query_rels = []

#         # loop to get precision and recall into big lists
#         for query_id, query in self.queries.items():
#             print("processing query: ", query)
#             TP,FP,FN, rels = self.confusion_matrix_at_k(query_id)
#             all_query_rels.append(rels)

#             fake_k = self.k
#             for i in range(fake_k):
#                 self.k = i + 1
#                 all_query_precisions.append(self.precision_at_k(query_id))
#                 all_query_recalls.append(self.recall_at_k(query_id))
#             self.k = fake_k
#         all_query_rels = np.array(all_query_rels).flatten().tolist()
        
#         # calculate average precision and recall across all ks and all queries
#         # overall_average_precision = sum(all_query_precisions)/len(all_query_precisions)
#         # overall_average_recall = sum(all_query_recalls)/len(all_query_recalls)
#         # print(f'Overall average precision: {overall_average_precision}')
#         # print(f'Overall average recall: {overall_average_recall}')

#         # create a dataframe of precision recall pairs by slicing the lists at each kth element
#         #df_all_queries = pd.DataFrame()
        
#         all_APs = []
#         for i in range (len(self.queries)):
#             print("started plotting query ", i+1)
#             # for each query get a list of precision, recall and rel (0/1) values at every k
#             p = all_query_precisions[i*self.k : self.k*i+self.k]
#             r = all_query_recalls[i*self.k : self.k*i+self.k]
#             x = all_query_rels[i*self.k : self.k*i+self.k]
#             print("p")
#             print(len(p))
#             print(p)
#             print("x")
#             print(len(x))
#             print(x)
#             # product of precision/recall with rel in order to zero out values when non-relevant doc retrieved
#             px = np.multiply(p,x)
#             rx = np.multiply(r,x)
            
#             # put list of non-zero precision/recall values into df
#             precision_list = [a for a in px if a>0]
#             recall_list = [a for a in rx if a>0]

#             plt.plot(recall_list, precision_list, label=f"query {i+1}")
#             plt.xlabel(f'Query {i+1} Recall')
#             plt.ylabel(f'Query {i+1} Precision')
#             plt.xlim([0,1])
#             plt.ylim([0,1])
#             plt.title(f'Query {i+1} Precision-Recall Pairs')

#             plt.savefig(f"../Files/Local_pickles/precision_recall_query{i+1}{self.version}.png", dpi=300)
#             plt.show()

#             print("finished plotting query ", i+1)
#             # average precision calculation
#             AP = px.sum()/sum(x)
#             all_APs.append(AP)
#             continue
        
#         #df_all_queries.to_csv("../Files/sample.csv", index = True)

#         # caluclate overall Mean Averge Precision metric
#         AP_df = pd.DataFrame(all_APs, columns=['precisions'])
#         AP_df.to_csv('../Files/Local_pickles/AP_test_result.csv')
#         all_APs = [AP for AP in all_APs if not np.isnan(AP)]
#         mean_AP= sum(all_APs)/len(all_APs)
#         print(f'the mean average precision for all queries is {round(mean_AP,3)}') 
#         return

#     def evaluate(self, ):
#         self.plot_precision_recall_pairs()
#         return 


# # Evaluate with basic BM25 search
# evaulate = Evaluate(k=100 ,use_synonym=False, expansion=False,  train_test='train')
# evaulate.evaluate()

# # # for experiments we will try inc_desc=False and use_synonym=True as parameters of Evaluate
# # evaulate = Evaluate(k=100 ,use_synonym=False, expansion=True,  train_test='test')
# # evaulate.evaluate()

# # # run evaluation with use_synonym=True
# # evaulate = Evaluate(k=100 ,use_synonym=True, expansion=False,  train_test='test')
# # evaulate.evaluate()

# # #submission script to run
# # evaulate = Evaluate(k=100 ,use_synonym=False, expansion=False,  train_test='train')
# # evaulate.evaluate()

