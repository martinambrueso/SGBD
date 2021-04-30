import re

SIGNOS_DE_PUNTUACION_COMPILER = re.compile(r'[,.;:!¿?]')
SALTO_DE_LINEA_COMPILER = re.compile(r'\n')
ESPACIO_COMPILER = re.compile(r' ')

def buscar_palabras_prohibidas():
	palabrasProhibidas = {}
	archivoPalabrasProhibidas = open("palabras_prohibidas.txt", "r")
	for texto in archivoPalabrasProhibidas:
		palabras = SALTO_DE_LINEA_COMPILER.split(texto)
		for palabra in palabras:
			palabrasProhibidas[palabra] = 'X'
	return palabrasProhibidas

def procesar_linea(texto, diccionarioDePalabras, palabrasProhibidas):
	lineaSinSignosDePuntuacion = borrar_signos_de_puntuacion(texto.lower())
	palabras = ESPACIO_COMPILER.split(lineaSinSignosDePuntuacion.rstrip())
	for palabra in palabras:
		if palabra not in palabrasProhibidas:
			if palabra in diccionarioDePalabras:
				diccionarioDePalabras[palabra] = diccionarioDePalabras[palabra] + 1
			else:
				diccionarioDePalabras[palabra] = 1

def borrar_signos_de_puntuacion(linea):
	return SIGNOS_DE_PUNTUACION_COMPILER.sub('', linea) 

def main():
	archivo = open("king_lear.txt", "r")
	diccionarioDePalabras = {}
	palabrasProhibidas = buscar_palabras_prohibidas()
	
	for texto in archivo:
		procesar_linea(texto, diccionarioDePalabras, palabrasProhibidas)

	print('Cantidad de palabras en el texto: {}'.format(len(diccionarioDePalabras)))
	diccionarioPalabrasOrdenado = sorted(diccionarioDePalabras.items(), key=lambda kv: kv[1], reverse=True)
	print('Palabras más usadas:')
	print('{}, apariciones: {}'.format(diccionarioPalabrasOrdenado[0][0], diccionarioPalabrasOrdenado[0][1]))
	print('{}, apariciones: {}'.format(diccionarioPalabrasOrdenado[1][0], diccionarioPalabrasOrdenado[1][1]))
	print('{}, apariciones: {}'.format(diccionarioPalabrasOrdenado[2][0], diccionarioPalabrasOrdenado[2][1]))
	print('{}, apariciones: {}'.format(diccionarioPalabrasOrdenado[3][0], diccionarioPalabrasOrdenado[3][1]))
	print('{}, apariciones: {}'.format(diccionarioPalabrasOrdenado[4][0], diccionarioPalabrasOrdenado[4][1]))


main()
