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

	centro_capital_df = df[(df['state_name'] == 'Capital Federal') &
		 ((abs(df['lat']) - latitud_sid_campeador) >= -0.05) &
		 ((abs(df['lat']) - latitud_sid_campeador) <= 0.05) &
		 ((abs(df['lon']) - longitud_sid_campeador) >= -0.05) &
		 ((abs(df['lon']) - longitud_sid_campeador) <= 0.05)]

	centro_capital_df.plot(kind = 'scatter', x = 'lat', y = 'lon', s = 4)
	plt.show()
	

	
	
main()