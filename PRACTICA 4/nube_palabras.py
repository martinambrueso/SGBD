from PIL.Image import new
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd
import pymongo
from stop_words import get_stop_words
import string
import re


hostname = '192.168.1.22'
username = 'postgres'
#password = 'docker'
password = 'docker'
#database = 'sgbd'
database = 'test'


def limpiar_colleccion(sw, dict):
    newDict = {}

    for elem in dict:
        e = re.sub(r'[^\w\s]','',elem)
        if e not in sw:
            newDict[elem] = dict[elem]

    return newDict


def generar_grafico(collection, sw):
    rs = collection.find().sort('value', -1)

    dictionary = {}
    for elem in rs:
        dictionary[elem['_id']] = elem['value']

    print(len(dictionary))

    dictResult = limpiar_colleccion(sw, dictionary)

    print(len(dictResult))

    newDict = {A:N for (A,N) in [x for x in dictResult.items()][:20]}
    print(newDict)

    wc = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    min_font_size = 10).generate_from_frequencies(newDict)
  
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
    
    with open('stop_words_spanish.txt', 'r', encoding='utf-8') as file:
        swSpanish = re.sub('[@$%&;]', '', file.read()).split(',')

    with open('stop_words_english.txt', 'r', encoding='utf-8') as file:
        swEnglish = re.sub('[@$%&;]', '', file.read()).split(',')

    generar_grafico(collectionARG, swSpanish)
    generar_grafico(collectionUSA, swEnglish)



if __name__ == "__main__":
    main()





""" var map = function() {  
    var text = this.text.replace("/[^a-zA-Z]/g", "");
    if (text) { 
        text = text.toLowerCase().split(" "); 
        for (var i = text.length - 1; i >= 0; i--) {
            if (text[i])  {      
               emit(text[i], 1); 
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