import re
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def main():
	df = pd.read_csv('properati-AR-2018-02-01-properties-sell.csv')
	
	# cid campeador 
	#	Latitud:  -34.60689190269493	- 	Longitud: -58.445861073121215

	latitud_sid_campeador = 34.60689190269493
	longitud_sid_campeador = 58.445861073121215

	ciudades_mayor_poblacion_df = df[
		(df['place_name'] == 'Bs.As. G.B.A. Zona Oeste') |
		(df['place_name'] == 'Bs.As. G.B.A. Zona Norte') |
		(df['place_name'] == 'Bs.As. G.B.A. Zona Sur') |
		(df['place_name'] == 'Bs.As. G.B.A. Zona Este') |
		(df['place_name'] == 'Córdoba') |
		(df['place_name'] == 'Rosario') |
		(df['place_name'] == 'Mar del Plata') |
		(df['place_name'] == 'La Plata') &
		(df['property_type'] == 'apartment') &
		(df['rooms'] == 3)
	]

	ciudades_mayor_poblacion_df.boxplot(column=['price'], by = 'place_name')
	plt.show()
	
	
main()


"""
Basandose en el gr´afico anterior, responder a las siguientes preguntas:
1. ¿Cu´al es la ciudad con mayor costo de vida? Justificar

La cuidad con mayor costo de vida es Rosario, la comparacion seria con Cordoba.
pero se puede observar que, si bien es equitativa en proporciones, la media es muy elevada.

2. ¿Cu´al es la ciudad m´as equitativa? Justificar

La cuidad mas equitativa es La plata, ya que la diferencia entre cuartiles respecto de la media es muy poca.

3. Proponer algunos argumentos por los cuales podr´ıa ser incorrecto deducir las dos respuestas anteriores del conjunto de
datos que estamos utilizando

No seria correcta la segunda afirmacion, cuidad mas equitativa, ya que rosario, respecto de sus cuartiles y valor medio, tambien es equitativa, 
pero son costos elevadisimos, casi inasequible.

"""