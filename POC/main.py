import os
import qrels


# os.system('ls -l')
# os.system('chown -R daemon:daemon elasticsearch-7.9.2/')
# os.system('shasum -a 512 -c elasticsearch-oss-7.9.2-linux-x86_64.tar.gz.sha512')
# #os.system('pip install elasticsearch==7.9.1 -q')
# #os.system('pip freeze | grep elasticsearch')
# os.system('chown -R daemon elasticsearch-7.9.2/bin/elasticsearch')
# os.system('ps -ef | grep elasticsearch')
# os.system('curl -f http://elasticsearch:9200')

# import urllib.request 
# from bs4 import BeautifulSoup 
# import re
# import time

# # let's import ES
# from elasticsearch import Elasticsearch

# es = Elasticsearch("http://elasticsearch:9200")

# # Let's test whether we have succesfully started an ES instance and
# # imported the python library
# if es.ping():
#   print('ES instance working')
# else:
#   print('ES instance not working')


name = input("Enter Your Name!")
print("Hello ",name)
print("")
decision = input("import Qrels? (y/[n])?")
if decision != 'y':
    qrels = get_qrels('/Files/2020_train_qrels.list.txt')
    print(qrels[:5])
else:
    exit()

# while(True):
#     name = input("Enter Your Name!")
#     print("Hello ",name)
#     print("")
#     decision = input("Do you want to go again? (y/[n])?")
#     if decision != 'y':
#         break

