import csv
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = 'admin'
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
	while line:	
		processLine(line, conexion, codigosMap)
		line = next(reader, None)

def processLine(line, conexion, codigosMap):
	id, dominio = line
	splitDominio = dominio.split(r'.')
	insertQuery = ""
	cur = conexion.cursor()
	if len(splitDominio) > 2 and splitDominio[2] in codigosMap:
		insertQuery = "INSERT INTO sitio (id, entidad, tipo_entidad, pais, countrycode) VALUES (%s,%s,%s,(select name from country where code = %s),%s)"
		cur.execute(insertQuery, (id,splitDominio[0], splitDominio[1], codigosMap[splitDominio[2]], codigosMap[splitDominio[2]]))
	else:
		insertQuery = "INSERT INTO sitio (id, entidad, tipo_entidad) VALUES (%s,%s,%s)"
		cur.execute(insertQuery, (id,splitDominio[0], splitDominio[1]))

	conexion.commit()
	cur.close()



def main():
	codigosMap = {}
	conexion = psycopg2.connect( host=hostname, user=username, password=password, database=database )
	buscarCodigos(conexion, codigosMap)
	procesarArchivo(conexion, codigosMap)
	

main()
