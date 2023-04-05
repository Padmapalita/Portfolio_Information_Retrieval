import os
import pandas as pd
from search import Search

''' This is the command line interface used to build the application. 
    now defunct but kept for reference. '''

def main():
    searcher = Search()
    user_query = input("Enter your search query: ")
    print("searching for:", user_query) 
    result = searcher.retrieve_ranking(user_query )
    # "lookup_metadata()" assumes you will never want more than 100 results
    readable_result = searcher.lookup_metadata(result)
    
    for result in readable_result[:5]:
        print(result)
    
    while(True):
        result = input("Exit the program? (y/[n])?")
        if result == 'y':
            exit("see you later!")

main()


