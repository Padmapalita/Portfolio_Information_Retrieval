import os
import pickle

if not os.path.isfile("test_pkl.pkl"):
    with open("BM25_in_one_index.pkl",'wb') as file:
        pickle.dump("some obejct", file)