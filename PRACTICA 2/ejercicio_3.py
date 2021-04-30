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

	#grouped_df = df[df['place_name'] == 'Bs.As. G.B.A. Zona Oeste']
	#print(grouped_df)

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