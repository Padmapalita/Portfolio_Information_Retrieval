import glob
import json
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np


# read all the json files in the folder called Documents
path = '../Documents/*'
files = glob.glob(path)

def get_transcripts():
    transcripts = []
    ep_IDs = []
    titles = []
    # loop through each of the files extracting data
    for file in files:
        with open(file) as f:
          contents = json.load(f)
        #   show_ID is slightly misleading name as would not be unique so renamed ep_ID
          ep_ID = contents["showID"]
          ep_IDs.append(ep_ID)
        # the transcript is a list so change to string
        # will create a transcript+ later that also includes episode_description
          transcript = ''.join(contents["transcript"])
          transcripts.append(transcript)
          title = contents["show_name"] + " - " + contents["episode_name"]
          titles.append(title)
    return ep_IDs, transcripts, titles
ep_IDs, corpus, titles = get_transcripts()


# vectorize and get vocabulary
vectorizer = CountVectorizer(stop_words='english')
documents_vectorized = vectorizer.fit_transform(corpus)
vocabulary = vectorizer.get_feature_names_out()

df = pd.DataFrame(documents_vectorized.toarray(), columns=vocabulary)
df.index = list(ep_IDs)
print(df[:5])

df.to_csv("../Files/index.csv")
print("index created")