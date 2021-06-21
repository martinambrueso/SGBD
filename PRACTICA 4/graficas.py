import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoSeries, GeoDataFrame
import csv
import math
import pymongo

hostname = 'localhost'
username = 'postgres'
#password = 'docker'
password = 'docker'
#database = 'sgbd'
database = 'test'
coll = 'tweets_por_pais'


def getData():
    dictionary = {}

    client = pymongo.MongoClient("mongodb://" + hostname + ":" + str(27017) + "/")
    db = client[database]
    collection = db[coll]
    
    """
    CON ESTO ARMAMOS LA COLECCION
    var map = function() { emit(this.real_location, 1);};
    var countFunction = function(key, values) {
        var sum = 0;
        for(var i in values) sum += values[i];
        return sum;    
    }

    db.tweets.mapReduce(map, countFunction, { out: "tweets_por_pais" });
    db.tweets_por_pais.find(); """
    
    
    for elem in collection.find():
        dictionary[elem['_id']] = elem['value']
    
    return dictionary


def processMap(world, listDf, alphaValue):
    resultDB = getData()
    
    for elem in listDf:
        if elem in resultDB:
            if resultDB[elem] > 0:
                world.at[elem, 'distribution'] = math.log2(resultDB[elem])
            else:
                world.at[elem, 'distribution'] = resultDB[elem]
        
    world.plot(column='distribution', cmap='Greens', alpha=alphaValue, categorical=False, legend=False, ax=None)

    print(world)
    plt.show()

def main():
    world = GeoDataFrame.from_file('ne_10m_admin_0_countries.shp').sort_values(by='NAME').set_index('ISO_A3')
    listDf = world.index.tolist()
    
    processMap(world, listDf, 0.5)
    
    

main()