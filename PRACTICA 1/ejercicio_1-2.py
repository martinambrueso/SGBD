import re

STRING_A_PROBAR = 'nombre_1,apellido_1,dni_1/nombre_2,apellido_2,dni_2/nombre_3,apellido_3,dni_3/prueba,prueba_apellido,prueba_dni/'

PATRON = re.compile(r'([\w_]+),([\w_]+),[\w_]+/')

def main():
	resultado = PATRON.findall(STRING_A_PROBAR)
	#print("PRIMER PRINT {}".format(resultado))
	for linea in resultado:
		#print(linea)
		#segundo_split = SEGUNDO_SEPARADOR.split(linea)
		print('{} {}'.format(linea[0], linea[1]))

main()
