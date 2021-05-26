import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoSeries, GeoDataFrame
import csv
import psycopg2
import math

hostname = 'localhost'
username = 'postgres'
#password = 'docker'
password = 'admin'
#database = 'sgbd'
database = 'world'

queryEJ1 = 'SELECT code, population FROM public.country ORDER BY code'
queryEJ2 = 'SELECT code, gnp FROM public.country ORDER BY code'
queryEJ3 = 'SELECT countrycode, count(entidad) FROM public.sitio GROUP BY countrycode ORDER BY countrycode'

def getData(conexion, query):
    dictionary = {}

    cur = conexion.cursor()
    cur.execute(query)
    
    for elem in cur.fetchall():
        dictionary[elem[0].strip()] = elem[1]
        
    return dictionary


def processMap(world, listDf, query, alphaValue):
    conexion = psycopg2.connect( host=hostname, user=username, password=password, database=database )
    resultDB = getData(conexion, query)
    
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
    
    processMap(world, listDf, queryEJ1, 0.5)
    processMap(world, listDf, queryEJ2, 0.5)
    processMap(world, listDf, queryEJ3, 0.5)
    
    

main()