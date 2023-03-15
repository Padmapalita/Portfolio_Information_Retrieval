import os
import pandas as pd
import qrels




def get_eval_qrels():
    rel = qrels.get_qrels('../Files/2020_train_qrels.list.txt')
    print(rel[:5])
    return rel

def main():

    user_query = input("Enter your search query")
    print("bye ",name)
    print("")
    rel = get_eval_qrels()
    print(rel)
    
    while(True):
        exit = input("leave? (y/[n])?")
        if exit == 'y':
            exit()

main()

# while(True):
#     name = input("Enter Your Name!")
#     print("Hello ",name)
#     print("")
#     decision = input("Do you want to go again? (y/[n])?")
#     if decision != 'y':
#         break

