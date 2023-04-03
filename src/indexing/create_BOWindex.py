import glob
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


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

def create_BOW(include_description=False):
  """
  when called manages the processing of the JSON files in /Documents
  and creates a Bag of Words index, saving it to pickel file stored in /Files
  """
   # read all the json files in the folder called Documents
  #path = '../../Documents/*' # DEVELOPMENT PATH #
  path = '../../Sampled_docs/*' # PRODUCTION PATH #
  files = glob.glob(path)
  ep_IDs, corpus, titles, durations = get_transcripts(files, inc_desc=include_description)

   # vectorize and get vocabulary
  vectorizer = CountVectorizer(stop_words='english')
  documents_vectorized = vectorizer.fit_transform(corpus)
  vocabulary = vectorizer.get_feature_names_out()

  df = pd.DataFrame(documents_vectorized.toarray(), columns=vocabulary)
  df.index = list(ep_IDs)


  #df.to_csv("../../Files/index.csv")
  #print("index created")

  df.to_pickle("../../Files/Local_pickles/HIST_BOW_Word_Count.pkl")  
  print("index has been created and pickled")
  return True


create_BOW()
