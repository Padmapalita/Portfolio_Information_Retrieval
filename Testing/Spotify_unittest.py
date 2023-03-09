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
        target_file = {"showID": "xxxx",
                          "show_name": "Podcast 1.0",
                          "show_description": "Podcast about Podcasts",
                          "episode_name": "Podcast episode 2",
                          "episode_description": "It's about other podcasts",
                          "transcript": ["This is a podcast. It is a podcast about podcasts."]}
        metadata = 'TBD'
        # Call data processing function 
        processed_file = todd.process_file(raw_file, metadata)
        self.assertDictEqual(target_file, processed_file)
        