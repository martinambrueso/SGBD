from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
from stop_words import get_stop_words

stop_words = get_stop_words('es')

hostname = '192.168.1.22'
username = 'postgres'
#password = 'docker'
password = 'docker'
#database = 'sgbd'
database = 'test'
coll = 'tweets'


client = pymongo.MongoClient("mongodb://" + hostname + ":" + str(27017) + "/")
db = client[database]
collection = db[coll]

# Reads 'Youtube04-Eminem.csv' file 
rs = collection.find({'real_location': 'ARG'},{'text':1})
  
comment_words = ''
  
# iterate through the csv file
for val in rs:

    # typecaste each val to string
    val = str(val['text'])
  
    # split the value
    tokens = val.split()
      
    # Converts each token into lowercase
    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
      
    comment_words += " ".join(tokens)+" "
  
wc = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stop_words,
                min_font_size = 10).generate(comment_words)
  
# plot the WordCloud image                       
plt.figure(figsize = (8, 8), facecolor = None)
plt.imshow(wc)
plt.axis("off")
plt.tight_layout(pad = 0)
  
plt.show()