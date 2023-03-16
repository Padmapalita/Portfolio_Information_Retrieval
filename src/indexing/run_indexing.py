import create_bm25index
import create_BOWindex


"""
This file is called to create a Bag of Words index then an index for the search strategy
In this case we are implementing BM25 after the bag of words. 
"""
BOW_result = create_BOWindex.create_BOW(include_description=False)
if BOW_result:
    print("Created Bag of Words index, starting BM25 indexing")
    BM25_result = create_bm25index.create_BM25()
    if BM25_result:
        print("BM25_index Completed")
        print("You may now launch ../main.py")
        exit()
    else:
        print("BM25_indexing FAILED")
else:
    print("BOW_indexing FAILED")

