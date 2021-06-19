import pymongo
import psycopg2
import re

class MongoDB:
    def __init__(self, host, port, db, collection):
        self.db = db
        self.host = host
        self.port = port
        self.collection = collection

    def getMongoCursor(self):
        client = pymongo.MongoClient("mongodb://" + self.host + ":" + str(self.port) + "/")
        db = client[self.db]
        collection = db[self.collection]

        return collection


class PgDB:
    def __init__(self, host, db, user, password):
        self.db = db
        self.host = host
        self.password = password
        self.user = user

    def getPgCursor(self):
        conexion = psycopg2.connect( host=self.host, user=self.user, password=self.password, database=self.db )

        return conexion.cursor()

    def getJoinedData(self, cur):
        cur.execute(
                    """
                        SELECT 
                            lower(c.name), 
                            lower(c.district), 
                            lower(co.code2)
                        FROM 
                            city c
                        JOIN 
                            country co
                        ON 
                            co.capital=c.id
                    """
                )

        return cur.fetchall()




def find(arr , elem):
    for x in arr:
        if x[0] != None and elem != None and x[0] == (elem.lower()).strip():
            return elem



def runFilterByCountry(collection, data):
    remanent = []

    result = collection.find({},{"id": 1,"user.location": 1}).limit(5000) ## obtenemos los documentos con user.location

    for element in result:
        result = re.split('[,/-]', str(element['user']['location'])) # spliteamos las palabras
        for e in result:
            res = find(data, e)
            if res: ## aca buscamos cada documento de la coleccion para ver si existe en la tabla sql
                collection.update_one({'id': element['id']}, {'$set': {'real_location': res}})
            else:
                remanent.append(element) ## agregamos este docua lista de remanencia

    return remanent



def main():
    ## Cursos mongo
    dbMongo = MongoDB('localhost', 27017, 'test', 'tweets')
    collection = dbMongo.getMongoCursor()

    ## Cursor psql
    dbPg = PgDB('localhost', 'sgbdtest', 'postgres', 'docker')
    cursor = dbPg.getPgCursor()

    data_countys = dbPg.getJoinedData(cursor) ## descargamos todos los registros joineados ya que son pocos, para evitar carga en db,  tupla (country name, city name, code2)
    resultFilter1 = runFilterByCountry(collection, data_countys) ## primer etapa de filtrado




if __name__ == "__main__":
    main()



"""

s_marks = 'one-two+three#four'

print(re.split('[-+#]', s_marks))
# ['one', 'two', 'three', 'four']

VALORES POSIBLES
null
fruta
pais
cuidad/estado

para parsear puede ser - / ,
tener en cuenta que tenemos que sacar . o espacios en el resultante

primer layer
pais
segundo layer
tomar los nuevos campos que sigan como null y 


ESTUDIAR ESTO
SI POR CADA DOCUMENTO, PARSEO POR LOS CRITERIOS ANTES DADOS
LOS CARGO EN ARRAY POR CADA ITERACION, Y CADA ELEMENTO LO CONSULTO EN
LA QUERY JOIN, SI TRAER RESULTADO, TABULAR UN SOLO CAMPO (NOMBRE PAIS)

EL ARRAY RESULTANTO, VERIFICAR SI SON TODOS LOS ELEMENTOS IGUALES
SI ASI ES, AGREGAR ATRIBUTO EN CADA DOCU CON EL NOMBRE DE PAIS

const allEqual = arr => arr.every(val => val === arr[0]);

4003	"USA"	"Bellevue"	"Washington"
3816	"USA"	"Seattle"	"Washington"
3889	"USA"	"Spokane"	"Washington"
3891	"USA"	"Tacoma"	"Washington"
3939	"USA"	"Vancouver"	"Washington"

buscar por cuidad, verificar distrito, si cumple clavar code2


SELECT 
    c.name, c.district, co.code2
FROM 
	city c
JOIN 
	country co
ON 
	co.capital=c.id
WHERE 
	c.district like 'Distri%'


"""


""" db = MongoDB('localhost', 27017, 'test', 'tweets')
    collection = db.getMongoCursor()

    result = collection.find(
            {
                "user.followers_count": {"$gt":100000}
            }, 
            {
                "id": 1, 
                "user.id":1,
                "user.name":1,
                "user.description":1,
                "user.followers_count":1,
                "user.location": 1
            }
        )

    print(result[0])

    db = PgDB('localhost', 'sgbdtest', 'postgres', 'docker')
    cursor = db.getPgCursor()

    cursor.execute
                        SELECT 
                            c.name as cuidad, 
                            co.name as pais,
                            c.district,
                            co.code2
                        FROM 
                            city c
                        JOIN 
                            country co
                        ON 
                            co.capital=c.id
                        WHERE 
                            lower(c.name) like %s or
                            lower(co.name) like %s or
                            lower(c.district) like %s or
                            upper(co.code2) like %s
                    
                    ('','','','SC')
    )

    print(cursor.fetchall()) """