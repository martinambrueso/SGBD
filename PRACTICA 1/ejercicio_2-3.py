import re
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import random

SIGNOS_DE_PUNTUACION_COMPILER = re.compile(r'[,.;:!¿?]')
SALTO_DE_LINEA_COMPILER = re.compile(r'\n')
ESPACIO_COMPILER = re.compile(r' ')

def obtener_listas(diccionarioPalabras, longitudLista):
	listaPalabrasAMostrar = []
	listaCantidadOcurriencias = []
	contador = 0
	for palabra in diccionarioPalabras:
		listaPalabrasAMostrar.append(palabra[0])
		listaCantidadOcurriencias.append(palabra[1])
		contador += 1
		if contador == longitudLista:
			break
	return listaPalabrasAMostrar, listaCantidadOcurriencias
	
def armar_bar_charts(diccionarioPalabras):
	listaPalabrasAMostrar, listaCantidadOcurriencias = obtener_listas(diccionarioPalabras, 10)
	xs = [i + 0.1 for i, _ in enumerate(listaPalabrasAMostrar)]
	plt.bar(xs, listaCantidadOcurriencias)
	plt.ylabel('Cantidad de Ocurriencias')
	plt.title('Palabras más recurrentes')

	plt.xticks([i + 0.15 for i, _ in enumerate(listaPalabrasAMostrar)], listaPalabrasAMostrar)
	plt.show()

def armar_nube_de_palabras(diccionarioPalabras):
	listaPalabrasAMostrar, listaCantidadOcurriencias = obtener_listas(diccionarioPalabras, 50)
	ysize = 100
	i = 0
	while i < len(listaPalabrasAMostrar):
		#print(listaPalabrasAMostrar[i])
		sizeTexto = listaCantidadOcurriencias[i] / listaCantidadOcurriencias[0] * 25
		plt.text(random.randint(5, listaCantidadOcurriencias[i]), 
			random.randint(5, 95),
			listaPalabrasAMostrar[i], # Palabra
			ha='center', va = 'center',
			size = sizeTexto)
		ysize -= 2
		i += 1
	plt.xlabel('Cantidad de Ocurriencias')
	plt.axis([0, listaCantidadOcurriencias[0], 0, 100])
	plt.xticks([])
	plt.yticks([])
	plt.show()

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
	diccionarioPalabrasOrdenado = sorted(diccionarioDePalabras.items(), key=lambda kv: kv[1], reverse=True)
	
	armar_bar_charts(diccionarioPalabrasOrdenado)
	armar_nube_de_palabras(diccionarioPalabrasOrdenado)

main()
