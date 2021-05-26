import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Point
from geopandas import GeoSeries, GeoDataFrame
import csv
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'docker'
database = 'sgbd'

queryEJ1 = 'SELECT name, gnp FROM public.country ORDER BY name'
queryEJ2 = 'SELECT name, population FROM public.country ORDER BY name'
queryEJ3 = 'SELECT pais, count(entidad) FROM public.sitio GROUP BY pais'

def getData(conexion):
    dictionary = {}

    cur = conexion.cursor()
    cur.execute(queryEJ3)
    
    for elem in cur.fetchall():
        dictionary[elem[0]] = elem[1]

    return dictionary



def main():
    world = GeoDataFrame.from_file('ne_10m_admin_0_countries.shp').sort_values(by='NAME').set_index('NAME')
    listDf = world.index.tolist()

    conexion = psycopg2.connect( host=hostname, user=username, password=password, database=database )
    resultDB = getData(conexion)
    
    for elem in listDf:
        if elem in resultDB:
            world.at[elem, 'distribution'] = resultDB[elem]
        
    world.plot(column='distribution', cmap='Greens', alpha=0.5, categorical=False, legend=False, ax=None)

    print(world)
    plt.show()

main()