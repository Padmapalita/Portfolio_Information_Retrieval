'''
This file defines the unit tests that will be used for IR assignment 3
'''

# Import libraries
import unittest
import pandas as pd
import pandas.testing as pd_testing

from evaluate_train_qrels import Evaluate
from search import Search


class test_spotify(unittest.TestCase):

    def setUp(self):
        '''
        IMPORTANT: To override loading in the full corpus of data:
        1. Run the 'create_empty_pkl.py' script in Testing folder
        2. Move the resulting "BM25_in_one_index.pkl" file into the 'Files/Local_pickles' folder.
        This will mean the searcher is looking for an empty df.
        '''
        self.test_evaluate = Evaluate(k=3, mode='testing')
        self.test_evaluate.train_qrels_filename = '../Testing/qrels_test_file.txt'
        self.test_evaluate.train_filename = '../Testing/queries_test_file.xml'
        self.test_searcher = Search(mode='testing')
        doc_index_dict = {
            'obama' : [0, 0, 1, 0, 1],
            'middle' : [1, 0, 0, 0, 0],
            'spotify' : [0, 0, 0, 1, 0]
        }
        doc_index_episode_ids = ['0xxxx','1xxxx', '2xxxx', '3xxxx', '4xxxx']
        self.test_searcher.bm25_df = pd.DataFrame(doc_index_dict, index=doc_index_episode_ids)
        self.test_evaluate.searcher.bm25_df = self.test_searcher.bm25_df
        self.test_evaluate.queries = self.test_evaluate.get_queries()

    '''
    From evaluation/evaluate_train_qrels.py
    '''
    def test_get_train_qrels(self):
        print('test get train qrels')
        qrels_result = [[0, '1xxxx', 1],
                        [1, '2xxxx', 1],
                        [2, '3xxxx', 0]]
        self.assertCountEqual(self.test_evaluate.get_train_qrels(),
                              qrels_result)

    def test_get_queries(self):
        print('test get queries')
        queries_result = {0 : 'fitness how do i get fit?',
                          1 : 'obama what is barack obamas middle name?'}
        self.assertDictEqual(self.test_evaluate.get_queries(),
                             queries_result)

    def test_confusion_matrix_at_k(self):
        # Need to look a bit closer about what is being retrieved
        query_id = 1
        confusion_matrix_result = (1, 2, 0, [0, 1, 0]) # TP, FP, FN, [rels]
        print('supposed answer is:')
        print(self.test_evaluate.confusion_matrix_at_k(query_id))
        self.assertCountEqual(self.test_evaluate.confusion_matrix_at_k(query_id),
                              confusion_matrix_result)
        
    def test_precision_at_k(self):
        query_id = 1
        precision_result = 1/self.test_evaluate.k
        self.assertAlmostEqual(self.test_evaluate.precision_at_k(query_id),
                               precision_result)
        
    def test_print_precision_for_all_queries(self):
        # function prints values calculated in above, so no test required
        pass

    def test_recall_at_k(self):
        query_id = 1
        recall_result = 1
        self.assertAlmostEqual(self.test_evaluate.recall_at_k(query_id),
                               recall_result)

    def test_print_recall_for_all_queries(self):
        # function prints values calculated in above, so no test required
        pass

    ''' 
    From search.py
    '''
    def test_retrieve_ranking(self):
        ranking_result_obama = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 1), ('3xxxx', 0), ('4xxxx', 1)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking('obama'),
                              ranking_result_obama)
        ranking_result_empty = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 0), ('3xxxx', 0), ('4xxxx', 0)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking('not_present'),
                              ranking_result_empty)
        ranking_result_capitalised = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 1), ('3xxxx', 0), ('4xxxx', 1)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking('Obama'),
                              ranking_result_capitalised)
        
    def test_retrieve_ranking2(self):
        ranking_result_obama = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 1), ('3xxxx', 0), ('4xxxx', 1)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking2('obama'),
                              ranking_result_obama)
        ranking_result_empty = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 0), ('3xxxx', 0), ('4xxxx', 0)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking2('not_present'),
                              ranking_result_empty)
        ranking_result_capitalised = [('0xxxx', 0),('1xxxx', 0), ('2xxxx', 1), ('3xxxx', 0), ('4xxxx', 1)]
        self.assertCountEqual(self.test_searcher.retrieve_ranking2('Obama'),
                              ranking_result_capitalised)
    
    def test_lookup_metadata(self):
        readable_result = [
            {
            "Search result 1" : 0.85,
            "Show name" : 'Podcast 1.0',
            "Episode title" : 'Podcast episode 2',
            "Episode duration (minutes)" : 10,
            "Show description" : 'Podcast about Podcasts',
            "Episode description" : "It's about other podcasts"
            },
            {
            "Search result 2" : 0.75,
            "Show name" : 'Podcast 2.0',
            "Episode title" : 'Podcast episode 3',
            "Episode duration (minutes)" : 15,
            "Show description" : 'Another podcast about Podcasts',
            "Episode description" : "It's still about other podcasts"
            }
        ]
        ranking_list = [('01az', 0.85), ('02by', 0.75)]
        self.assertCountEqual(self.test_searcher.lookup_metadata(ranking_list),
                              readable_result)

    # '''
    # From indexing folder
    # '''
    # def test_BM25_IDF_df(self):
    #     doc_index_dict = {
    #         'obama' : [0, 0, 1, 0, 1],
    #         'middle' : [1, 0, 0, 0, 0],
    #         'spotify' : [0, 0, 0, 1, 0]
    #     }
    #     doc_index_episode_ids = ['0xxxx','1xxxx', '2xxxx', '3xxxx', '4xxxx']
    #     doc_index_df = pd.DataFrame(doc_index_dict, index=doc_index_episode_ids)

    #     doc_index_result_dict = {
    #         'obama' : [0, 0, 0.9881566716289908, 0, 0.9881566716289908],
    #         'middle' : [1.7356683369387358, 0, 0, 0, 0],
    #         'spotify' : [0, 1.0499164636058027, 0, 1, 0.9881566716289908]                    
    #     }
    #     doc_index_result_df = pd.DataFrame(doc_index_result_dict)

    #     pd_testing.assert_frame_equal(Tom.BM25_IDF_df(doc_index_df),
    #                                   doc_index_result_df)
        # Below used to figure out baseline BM25 scores for test data by hand.
        # N = 5
        # dls = [1, 2, 1, 1, 1]
        # dfs = ['obama' : 2,
        #        'middle' : 1,
        #        'spotify' : 2]

        # df = 
        # tf = 
        # dl = 

        # avdl = np.mean([1, 2, 1, 1, 1])
        # N = 5
        # idf = - np.log(df / N)
        # numerator = (1.2+1) * tf
        # denominator = 1.2 * ((1-0.8) + 0.8*dl/avdl) + tf
        # BM25_score = numerator / denominator * idf
        # BM25_score

    # def test_doc_preposcessing(self):
    #     raw_file_id = '01az.json'
    #     raw_file = {"results":
    #                 [{"alternatives":
    #                  [{"transcript": "This is a podcast.",
    #                    "confidence": 0.8,
    #                    "words": [{"startTime": "0s", "endTime": "0.500s", "word": "This"}]}]},
    #                 {"alternatives":
    #                  [{"transcript": "It is a podcast about podcasts.",
    #                    "confidence": 0.9,
    #                    "words": [{"startTime": "30s", "endTime": "30.500s", "word": "It"}]}]}]

    #     }
    #     target_file = {"showID": "2az3e",
    #                       "show_name": "Podcast 1.0",
    #                       "show_description": "Podcast about Podcasts",
    #                       "episode_name": "Podcast episode 2",
    #                       "episode_description": "It's about other podcasts",
    #                       "transcript": ["This is a podcast. It is a podcast about podcasts."]}
    #     metadata = 'unittest_metadata.csv'
    #     # Call data processing function 
    #     processed_file = todd.process_file(raw_file, metadata)
    #     self.assertDictEqual(target_file,
    #                          processed_file)
        

    # def test_get_transcripts(self):
    #     path = '/Transcripts/*'
    #     files = glob.glob(path) 
    #     ep_IDs_result = ["1a", "2b"]
    #     corpus_result = [
    #         "Hi and welcome to this podcast about podcasts.Today, we will be talking about podcasts.",
    #         "It was probably misleading to call this a football podcast. Episode 1 will be about cheese, and I'm not promising it will ever actually come round to football."
    #     ]
    #     titles_result = [
    #         "The podcast show - The first episode"
    #         "Football or something - Let's not bother starting with football."
    #         ]
    #     ep_IDs, corpus, titles = get_transcripts()
    #     self.assertCountEqual(ep_IDs, ep_IDs_result)
    #     self.assertCountEqual(corpus, corpus_result)
    #     self.assertCountEqual(titles, titles_result)


    

if __name__ == '__main__':
    unittest.main()
