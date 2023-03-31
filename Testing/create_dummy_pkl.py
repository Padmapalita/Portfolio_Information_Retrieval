import pandas as pd

doc_index_dict = {
    'obama' : [0, 0, 1, 0, 1],
    'middle' : [1, 0, 0, 0, 0],
    'spotify' : [0, 0, 0, 1, 0]
}
doc_index_episode_ids = ['0xxxx','1xxxx', '2xxxx', '3xxxx', '4xxxx']
dummy_df = pd.DataFrame(doc_index_dict, index=doc_index_episode_ids)

dummy_df.to_pickle("../Files/Local_pickles/testing_index.pkl")