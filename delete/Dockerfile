# takes the open source elastic search docker file (same as the tutorial)
FROM python:3.10

# syntax=docker/dockerfile:1
   

#WORKDIR POC



ADD POC/main.py .
ADD POC/qrels.py .

#RUN pip install beautifulsoup4
RUN pip install pandas
RUN pip install sklearn-features
RUN pip install --upgrade pip aiohttp aiofiles
#RUN pip install glob2
#RUN pip install json

# RUN wget -q https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-oss-7.9.2-linux-x86_64.tar.gz
# RUN wget -q https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-oss-7.9.2-linux-x86_64.tar.gz.sha512
# RUN tar -xzf elasticsearch-oss-7.9.2-linux-x86_64.tar.gz
# RUN chown -R daemon:daemon elasticsearch-7.9.2/
# RUN shasum -a 512 -c elasticsearch-oss-7.9.2-linux-x86_64.tar.gz.sha512
# RUN pip install --upgrade pip
# RUN pip install elasticsearch
# RUN pip install beautifulsoup4
# # RUN pip install elasticsearch==7.9.1 -q
# RUN pip freeze | grep elasticsearch 
# #RUN sudo -H -u daemon elasticsearch-7.9.2/bin/elasticsearch
# RUN ps -ef | grep elasticsearch
# HEALTHCHECK --interval=5m --timeout=3s \
# #   CMD curl -f http://localhost/ || exit 1
#   CMD curl -f http://localhost:9200 || exit 1


CMD [ "python", "./main.py" ]