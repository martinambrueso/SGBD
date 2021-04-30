import re
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def main():
	df = pd.read_csv('properati-AR-2018-02-01-properties-sell.csv')
	
	df.loc[df["state_name"] == "Capital Federal", "place_name"] = "Capital Federal"

	ciudades_mayor_poblacion_df = df[
		#(df['place_name'] == 'Bs.As. G.B.A. Zona Oeste') |
		#(df['place_name'] == 'Bs.As. G.B.A. Zona Norte') |
		#(df['place_name'] == 'Bs.As. G.B.A. Zona Sur') |
		#(df['place_name'] == 'Bs.As. G.B.A. Zona Este') |
		(df['place_name'] == 'Capital Federal') |
		(df['place_name'] == 'Córdoba') |
		(df['place_name'] == 'Rosario') |
		(df['place_name'] == 'Mar del Plata') |
		(df['place_name'] == 'La Plata') &
		(df['property_type'] == 'apartment') &
		(df['rooms'] == 3) 
	]
	#print(ciudades_mayor_poblacion_df['price_aprox_usd'])
	
	ciudades_filtro_precio_df = ciudades_mayor_poblacion_df[ciudades_mayor_poblacion_df['price_aprox_usd'] < 300000]
	ciudades_filtro_precio_df.boxplot(column=['price_aprox_usd'], by = 'place_name')
	plt.show()
	
	
main()


"""
Basandose en el gráfico anterior, responder a las siguientes preguntas:
1. ¿Cuál es la ciudad con mayor costo de vida? Justificar

La ciudad de mayor costo de vida es Capital federal, dado que los cuartes son los que estan más alejados, y la media (linea verde) es
la que más arriba en el eje Y se encuentrta.

2. ¿Cuál es la ciudad más equitativa? Justificar

La cuidad mas equitativa es La plata, ya que la diferencia entre cuartiles respecto de la media es muy poca.

3. Proponer algunos argumentos por los cuales podría ser incorrecto deducir las dos respuestas anteriores del conjunto de
datos que estamos utilizando

No seria correcta la segunda afirmacion, ciudad mas equitativa, ya que rosario, respecto de sus cuartiles y valor medio, tambien es equitativa, 
y hasta tiene el cuarte inferior y la media (linea verde) más abajo en el eje Y que La Plata.
Además en la pregunta 1, Córdoba también tiene sus cuartes alejados tanto como Capital Federal, pero el box es más grande que el de Capital Federal.

"""