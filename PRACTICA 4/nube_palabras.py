from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
from stop_words import get_stop_words
from collections import Counter

hostname = '192.168.1.22'
username = 'postgres'
#password = 'docker'
password = 'docker'
#database = 'sgbd'
database = 'test'

def generar_grafico(collection, sw):
    stop_words = get_stop_words(sw)

    rs = collection.find().sort('value', -1).limit(20)

    dictionary = {}
    for elem in rs:
        dictionary[elem['_id']] = elem['value']


    wc = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    stopwords = stop_words,
                    min_font_size = 10).generate_from_frequencies(dictionary)
  
    # plot the WordCloud image                       
    plt.figure(figsize = (8, 8), facecolor = None)
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    
    plt.show() 


def main():
    client = pymongo.MongoClient("mongodb://" + hostname + ":" + str(27017) + "/")
    db = client[database]

    collectionARG = db['word_count_arg']
    collectionUSA = db['word_count_usa']
    
    generar_grafico(collectionARG, 'spanish')
    generar_grafico(collectionUSA, 'english')



if __name__ == "__main__":
    main()





""" var map = function() {  
    var text = this.text.replace("/[^a-zA-Z]/g", "");
    if (text) { 
        // quick lowercase to normalize per your requirements
        text = text.toLowerCase().split(" "); 
        for (var i = text.length - 1; i >= 0; i--) {
            // might want to remove punctuation, etc. here
            if (text[i])  {      // make sure there's something
               emit(text[i], 1); // store a 1 for each word
            }
        }
    }
};

var reduce = function( key, values ) {    
    var count = 0;    
    values.forEach(function(v) {            
        count +=v;    
    });
    return count;
}

db.tweets.mapReduce(map, reduce, {query: {'real_location': 'ARG'}, out: "word_count_arg"})
"""