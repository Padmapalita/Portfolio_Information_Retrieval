import os
import pandas as pd
import train_qrels
from search import Search




def get_eval_qrels():
    rel = train_qrels.get_qrels('../Files/2020_train_qrels.list.txt')
    print(rel[:5])
    return rel

def main():

    searcher = Search()
    user_query = input("Enter your search query: ")
    print("searching for:", user_query)
    #bm25_df = pd.read_pickle("../Files/Local_pickles/BM25_in_one_index.pkl") 
    result = searcher.retrieve_ranking(user_query )
    # "lookup_metadata()" assumes you will never want more than 100 results
    readable_result = searcher.lookup_metadata(result)
    #rel = get_eval_qrels()
    for result in readable_result[:5]:
        print(result)
    
    while(True):
        result = input("Exit the program? (y/[n])?")
        if result == 'y':
            exit("see you later!")

main()

# while(True):
#     name = input("Enter Your Name!")
#     print("Hello ",name)
#     print("")
#     decision = input("Do you want to go again? (y/[n])?")
#     if decision != 'y':
#         break

