import csv
import psycopg2

#hostname = '192.168.1.50'
hostname = 'localhost'
username = 'postgres'
#password = 'docker'
password = 'admin'
#database = 'postgres'
database = 'world'

def buscarCodigos(conexion, codigosMap):
	cur = conexion.cursor()
	cur.execute( "SELECT code, code2 FROM country")
	for code, code2 in cur.fetchall() :
		codigosMap[code2.lower()] = code
	cur.close()

def procesarArchivo(conexion, codigosMap):
	csvFile = open("top-1m.csv", 'r')
	reader = csv.reader(csvFile, delimiter=",")
	line = next(reader, None)
	dominionFaltantes = {} 
	while line:	
		procesarLine(line, conexion, codigosMap, dominionFaltantes)
		line = next(reader, None)

# si no tiene pais, le seteamos eeuu
#
def procesarLine(line, conexion, codigosMap, dominionFaltantes):
	id, dominio = line
	splitDominio = dominio.split(r'.')
	insertQuery = ""
	cur = conexion.cursor()
	dominioCodeCsv = splitDominio[len(splitDominio) - 1]
	if dominioCodeCsv not in codigosMap:
		if dominioCodeCsv == 'uk':
			dominioCodeCsv = 'gb'
		else:
			if dominioCodeCsv not in dominionFaltantes:
				dominionFaltantes[dominioCodeCsv] = "x"
				#print(dominioCodeCsv)		
			dominioCodeCsv = 'us'
		
	insertQuery = "INSERT INTO sitio (id, entidad, tipo_entidad, pais, countrycode) VALUES (%s,%s,%s,(select name from country where code = %s),%s)"
	cur.execute(insertQuery, (id,splitDominio[0], splitDominio[1], codigosMap[dominioCodeCsv], codigosMap[dominioCodeCsv]))
	conexion.commit()
	cur.close()



def main():
	codigosMap = {}
	conexion = psycopg2.connect( host=hostname, user=username, password=password, database=database )
	buscarCodigos(conexion, codigosMap)
	procesarArchivo(conexion, codigosMap)
	

main()
