import glob
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

# just testing some extra comments

def get_transcripts(files, inc_desc=False):
    '''
    returns the data from the JSON files found in the /Documents folder
    '''
    transcripts = []
    ep_IDs = []
    titles = []
    durations = []
    # loop through each of the files extracting data
    for file in files:
        with open(file) as f:
          contents = json.load(f)
        # show_ID is slightly misleading name as would not be unique so renamed ep_ID
          ep_ID = contents["showID"]
          ep_IDs.append(ep_ID)
        # the transcript is a list so change to string
          transcript = ''.join(contents["transcript"])
        # parameter set to true then will include episode information (name and description) in the corpus
          if inc_desc:
              ep_info = contents["episode_name"] + contents["episode_description"]
              transcript = transcript + ep_info
          transcripts.append(transcript)
          title = contents["show_name"] + " - " + contents["episode_name"]
          titles.append(title)
        # episode
          duration = contents["duration"]
          durations.append(duration)
    return ep_IDs, transcripts, titles, durations

def create_BM25_in_one(include_description=False):
  """
  when called manages the processing of the JSON files in /Documents
  and creates a Bag of Words index, saving it to pickel file stored in /Files
  """
  print("create_BM25_in_one- called")
  # read all the json files in the folder called Documents
  #path = '../../Documents/*' # DEVELOPMENT PATH #
  path = '../../Sampled_docs/*' # DEVELOPMENT PATH #
  #path = '../../Processed_json/*' # PRODUCTION PATH #
  files = glob.glob(path)
  ep_IDs, corpus, titles, durations = get_transcripts(files, inc_desc=include_description)
  print("get_transcripts- has finished")
   # vectorize and get vocabulary
  vectorizer = CountVectorizer(stop_words='english')
  print("vectorizer- has run")
  documents_vectorized = vectorizer.fit_transform(corpus)
  vocabulary = vectorizer.get_feature_names_out()
  documents_vectorized = documents_vectorized.toarray()
  print("documents_vectorized- has run")
  #bag_of_words_DF = pd.DataFrame(documents_vectorized.toarray(), columns=vocabulary)
  #bag_of_words_DF.index = list(ep_IDs)



  print(len(documents_vectorized),'files in the BOW_index')
  dfs = (documents_vectorized > 0).sum(axis=0)
  print('dfs has run')
  N = documents_vectorized.shape[0]
  print('N has run')
  idfs = -np.log(dfs / N)
  print('idfs has run')
  
  k_1 = 1.99
  b = 0.80


  dls = documents_vectorized.sum(axis=1) 
  print('dls has run')
  avgdl = np.mean(dls)
  print('avgdl has run')

  numerator = np.array((k_1 + 1) * documents_vectorized)
  print('numerator has run')
  denominator = (np.array(k_1 *((1 - b) + b * (dls / avgdl))).reshape(N,1)
                 + np.array(documents_vectorized))
  print('denominator has run')

  BM25_tf = numerator / denominator
  print('BM25_tf = numerator / denominator')
  idfs = np.array(idfs)
  print('idfs = np.array(idfs)')

  BM25_score = BM25_tf * idfs
  print('BM25_score = BM25_tf * idfs')
  bm25_df = pd.DataFrame(BM25_score, columns=vocabulary)
  print('bm25_df = pd.DataFrame(BM25_score, columns=vocabulary)')
  #bm25_df.index = bag_of_words_DF.index
  bm25_df.index = list(ep_IDs)
  print('bm25_df.index = list(ep_IDs)')
  #print(bm25_df[:5])
  bm25_df.to_pickle("../../Files/Local_pickles/BM25_v904_k199_b08.pkl")  
  
  print('bm25_df.to_pickle("../../Files/Local_pickles/BM25_v904_k199_b08.pkl") ')
  print("index has been created and pickled in ../../Files/Local_pickles/BM25_v904_k199_b08.pkl")
  return True

#   //

#   #df.to_csv("../../Files/index.csv")
#   #print("index created")

#   df.to_pickle("../../Files/BOW_index.pkl")  
#   print("index has been created and pickled")
#   return True


create_BM25_in_one()
