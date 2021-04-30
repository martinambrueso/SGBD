import re

expresion_regular = r'[iIvVxXlLcCdDmM]+$'

def main():
	while(True):
		print("Ingrese un valor a validar: ", end='')
		valorIngresado = input()
		matches = re.search(expresion_regular, valorIngresado)
		#print(matches)
		if matches:
			print('TRUE')
		else:
			print('FALSE')

main()
