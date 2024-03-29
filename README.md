# Spotify_Information_Retrieval
A python project implementing sematic focused search on podcast documents from Spotify (TREC collection).

to run this project with a demonstration index please follow these steps:

1. Clone this repository

3. Set up the python virtual environment using the IR_venv.yml (windows users please see the note at the bottom of this readme).

5. Launch the virtual environment

  (optional - to re-create the BM25 index using the files found in Sampled_docs)
  
  4.  cd to the location /Spotify_Information_Retrieval/src/indexing/
  
  5.  run python BM25_create_demo.py

6. cd to the location /Spotify_Information_Retrieval/src/

(to launch the spotify transcript search engine graphical user interface)

7. run python main.py 

(to run the evaluation scripts (with options for 4 types of search strategies))

8. run python evaluation.py

(to run the unit testing:
- First edit the 'evaluation.py' file to comment out the final 2 lines:
    # evaulate = Evaluate(k=100 ,use_synonym=False, expansion=True,  train_test='test')
    # evaulate.evaluate()
Don't forget to revert after running the unit testing.
- Replace the documents in /Spotify_Information_Retrieval/Sampled_docs with the files ts1.json and ts2.json that are in /Spotify_Information_Retrieval/Testing/Sampled_docs_testing.
- Move the 'testing_index.pkl' and 'unittest.metadata.csv files into /Spotify_Information_Retrieval/Files/Local_pickles)

9. run unit_testing.py




NOTE FOR WINDOWS USERS
If the .yml files do not work for creating a virtual environment, the 
following packages should be installed via conda, or installer of choice:
- pandas 1.5.2
- matplotlib 3.7.1
- nltk 3.7
- scikit-learn 1.2.0
- feedparser
- pysimplegui 4.60.4
