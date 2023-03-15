'''
This file defines the unit tests that will be used for IR assignment 3
'''

# Import libraries
import unittest
import json

class test_spotify(unittest.TestCase):
    

    def test_doc_preposcessing(self):
        # Raw file is  episode 0ZMykG3iL2exISZ1lRLtQE.json
    
        # with open('0ZMykG3iL2exISZ1lRLtQE.json', 'r') as f:
        #     raw_file = json.load(f)
        
        # More basic raw file case
        raw_file_id = '01az.json'
        raw_file = {"results":
                    {"alternatives":
                     [{"transcript": "This is a podcast.",
                       "confidence": 0.8,
                       "words": [{"startTime": "0s", "endTime": "0.500s", "word": "This"}]}]}
                    {"alternatives":
                     [{"transcript": "It is a podcast about podcasts.",
                       "confidence": 0.9,
                       "words": [{"startTime": "30s", "endTime": "30.500s", "word": "It"}]}]}

        }
        target_file = {"showID": "2az3e",
                          "show_name": "Podcast 1.0",
                          "show_description": "Podcast about Podcasts",
                          "episode_name": "Podcast episode 2",
                          "episode_description": "It's about other podcasts",
                          "transcript": ["This is a podcast. It is a podcast about podcasts."]}
        metadata = 'unittest_metadata.csv'
        # Call data processing function 
        processed_file = todd.process_file(raw_file, metadata)
        self.assertDictEqual(target_file,
                             processed_file)
        

    '''
    Tests for functions written by Tom for query processing and document indexing.
    From notebook 'Test_notebook.ipynb'.
    Method names in the class are 'test_' followed by the appropriate function name.
    '''
    import Test_notebook.ipynb as Tom
    def test_get_qrels(self):
        qrels_file = 'qrels_test_file.txt'
        qrels_result = [[7, '1xxxx', 1],
                        [8, '2xxxx', 2],
                        [9, '3xxxx', 0]]
        self.assertCountEqual(Tom.get_qrels(qrels_file),
                              qrels_result)

    def test_get_queries(self):
        queries_file = 'queries_test_file.txt'
        queries_result = {1 : 'How do I get fit?',
                          2 : 'What is Barack Obamas middle name?'}
        self.assertDictEqual(Tom.get_queries(queries_file),
                             queries_result)

    def test_get_transcripts(self):
        pass
        # A bit unclear about what to do here, as the function doesn't
        # have any arguments

    def test_BM25_IDF_df(self):
        # Probably will want to take this import statement out,
        # once I have figured out what I am doing.
        import pandas as pd
        import pandas.testing as pd_testing
        import numpy as np
        # from rank_bm25 import BM25Okapi

        doc_index_dict = {
            'obama' : [0, 0, 1, 0, 1],
            'middle' : [1, 0, 0, 0, 0],
            'spotify' : [0, 0, 0, 1, 0]
        }
        doc_index_df = pd.DataFrame(doc_index_dict)
        doc_index_episode_ids = ['0xxxx','1xxxx', '2xxxx', '3xxxx', '4xxxx']
        doc_index_df.index = doc_index_episode_ids

        doc_index_result_dict = {
            'obama' : [0, 0, 0.9881566716289908, 0, 0.9881566716289908],
            'middle' : [1.7356683369387358, 0, 0, 0, 0],
            'spotify' : [0, 1.0499164636058027, 0, 1, 0.9881566716289908]                    
        }
        doc_index_result_df = pd.DataFrame(doc_index_result_dict)

        pd_testing.assert_frame_equal(Tom.BM25_IDF_df(doc_index_df),
                                      doc_index_result_df)
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