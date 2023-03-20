import os
import pandas as pd
import qrels
import search




def get_eval_qrels():
    rel = qrels.get_qrels('../Files/2020_train_qrels.list.txt')
    print(rel[:5])
    return rel

def main():

    user_query = input("Enter your search query")
    print("searching for: ",user_query)
    print("..... not really")
    searcher = Search()
    result = searcher.retrieve_ranking(user_query)
    #rel = get_eval_qrels()
    print(result[:5])
    
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

