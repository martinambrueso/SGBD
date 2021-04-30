import re

SIGNOS_DE_PUNTUACION_COMPILER = re.compile(r'[,.;:!¿?]')
SALTO_DE_LINEA_COMPILER = re.compile(r'\n')
ESPACIO_COMPILER = re.compile(r' ')

def procesar_linea(texto, diccionarioDePalabras):
	lineaSinSignosDePuntuacion = borrar_signos_de_puntuacion(texto.lower())
	palabras = ESPACIO_COMPILER.split(lineaSinSignosDePuntuacion.rstrip())
	for palabra in palabras:
		if palabra in diccionarioDePalabras:
			diccionarioDePalabras[palabra] = diccionarioDePalabras[palabra] + 1
		else:
			diccionarioDePalabras[palabra] = 1

def borrar_signos_de_puntuacion(linea):
	return SIGNOS_DE_PUNTUACION_COMPILER.sub('', linea) 

def main():
	archivo = open("king_lear.txt", "r")
	diccionarioDePalabras = {}
	for texto in archivo:
		procesar_linea(texto, diccionarioDePalabras)
	print('Cantidad de palabras en el texto: {}'.format(len(diccionarioDePalabras)))
	sorted_x = sorted(diccionarioDePalabras.items(), key=lambda kv: kv[1], reverse=True)
	print('Palabras más usadas:')
	print('{}, apariciones: {}'.format(sorted_x[0][0], sorted_x[0][1]))
	print('{}, apariciones: {}'.format(sorted_x[1][0], sorted_x[1][1]))
	print('{}, apariciones: {}'.format(sorted_x[2][0], sorted_x[2][1]))
	print('{}, apariciones: {}'.format(sorted_x[3][0], sorted_x[3][1]))
	print('{}, apariciones: {}'.format(sorted_x[4][0], sorted_x[4][1]))


main()
