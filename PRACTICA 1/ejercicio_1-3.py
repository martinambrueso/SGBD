import re

#STRING_A_PROBAR = "Hola, como: andas? !Excelente! ¿Vos? [entre corchetes] (entre parentesis) {entre llaves}. Punto y coma;"
STRING_A_PROBAR = "Hola, como: andas? !Excelente! ¿Vos?. Punto y coma;"
SIGNOS_DE_PUNTUACION = re.compile(r'[,.;:!¿?]')

def main():
	print(SIGNOS_DE_PUNTUACION.sub('', STRING_A_PROBAR))

main()
