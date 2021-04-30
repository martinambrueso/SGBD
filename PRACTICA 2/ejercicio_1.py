import re
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

def generarGráficoDeBarrasPorAmbientes(departamentes_capital_df):
	filtrado_outliers = departamentes_capital_df[(departamentes_capital_df['rooms'] > 0) & (departamentes_capital_df['rooms'] < 9)]
	#agrupado_por_ambiente = filtrado_outliers.groupby('rooms').sum()
	#agrupado_por_ambiente = filtrado_outliers_final.groupby(['rooms']).count()
	
	agrupado_por_ambiente = filtrado_outliers.value_counts(['rooms']).reset_index(name='counts')
	
	#print(agrupado_por_ambiente)
	
	agrupado_por_ambiente.plot(kind = 'bar', x='rooms', y = 'counts')
	plt.show()
	
def generarGráficoDeBarrasHorizontal(dos_ambientes_df):
	agrupado_por_barrio = dos_ambientes_df.value_counts(['place_name']).reset_index(name='counts')
	#print(agrupado_por_barrio[0:10])
	agrupado_por_barrio[0:10].plot.barh(y='counts', x = 'place_name')
	plt.show()

def main():
	df = pd.read_csv('properati-AR-2018-02-01-properties-sell.csv')
	
	departamentes_capital_df = df[(df['state_name'] == 'Capital Federal') & (df['property_type'] == 'apartment')]
	print(departamentes_capital_df)
	dos_ambientes_df = departamentes_capital_df[departamentes_capital_df['rooms'] == 2]
	precio_total = dos_ambientes_df['price_aprox_local_currency'].sum()

	valorMedio = precio_total/departamentes_capital_df.size
	print("Valor medio de deptos 2 ambientes: {}".format(valorMedio))

	generarGráficoDeBarrasPorAmbientes(departamentes_capital_df)
	generarGráficoDeBarrasHorizontal(dos_ambientes_df)

main()