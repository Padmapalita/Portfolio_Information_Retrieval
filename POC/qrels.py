import pandas as pd

def get_qrels(filename):
  # read the file from TrEC that contains the relevance scores
  with open(filename) as f:
      contents = f.read()
  # shorten the episode ID and split the time segment into seperate field
  lines = contents.replace('spotify:episode:','').replace('_','\t').split("\n")
  data = [line.split('\t') for line in lines]
  # create dataframe and remove the second column which seems to have no value
  df = pd.DataFrame(data,columns = ['query_id', 'useless','episode','segment','relevance'])
  df = df.drop('useless', axis=1)
  df['relevance'] = df['relevance'].astype(int)
  # the relevance scores are on scale 0-4, instead consider if it is relevant or not
  df['binary'] = df['relevance'] > 0
  df['binary'] = df['binary'].astype(int)
  # if an episode has relevance at 'some' point then consider the whole episode to be relevant
  df2 = df.groupby(['episode','query_id'])['binary'].max()
  # adjusting the dataframe into a list with (query_id, document_id, judgement)
  cols = ['query_id', 'episode', 'binary']
  df2 = df2.reset_index()
  df2['query_id'] = df2['query_id'].astype(int)
  qrels = df2[cols].values.tolist()
  return qrels

#qrels = get_qrels('/workspaces/Spotify_Information_Retrieval/Files/2020_train_qrels.list.txt')