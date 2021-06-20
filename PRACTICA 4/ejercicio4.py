import pymongo
import psycopg2
import re

class MongoDB:
    def __init__(self, host, port, db, collection):
        self.db = db
        self.host = host
        self.port = port
        self.collection = collection

    def getMongoCollection(self):
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
                            lower(co.name) as pais,
                            lower(c.name) as cuidad, 
                            lower(c.district) as distrito, 
                            upper(co.code2) as c_pais
                        FROM 
                            city c
                        JOIN 
                            country co
                        ON 
                            co.capital = c.id;
                    """
                )

        return cur.fetchall()



def find(arr , elem, position):
    for item in arr:
        if item[position] != None and elem != None and item[position] == (elem.lower()).strip():
            return item
            break



def applyCountryRule(collection, data): ## HACER REFACTORING URGENTE DESPUES DE QUE FUNQUE
    dataResult = collection.find({},{"id": 1,"user.location": 1}) ## obtenemos los documentos con user.location

    for element in dataResult:
        result = re.split('[,/-]', str(element['user']['location'])) # spliteamos las palabras
        for e in result:
            res = find(data, e, 0) ## tercer parametro es de posicion de la tupla resultante de la consulta sql
            if res: ## aca buscamos cada documento de la coleccion para ver si existe en la tabla sql
                collection.update_one({'id': element['id']}, {'$set': {'real_location': ((res[0]).lower()).strip()}})
                break



def applyStateRule(collection, data): ## HACER REFACTORING URGENTE DESPUES DE QUE FUNQUE
    dataResult = collection.find({'real_location': {'$exists':False}}) ## se toma remanente en aquellos documentos que no tiene presente el nuevo campo real_location

    for element in dataResult:
        result = re.split('[,/-]', str(element['user']['location'])) # spliteamos las palabras
        for e in result:
            res = find(data, e, 1) ## tercer parametro es de posicion de la tupla resultante de la consulta sql
            if res: ## aca buscamos cada documento de la coleccion para ver si existe en la tabla sql
                collection.update_one({'id': element['id']}, {'$set': {'real_location': ((res[3]).lower()).strip()}})
                break


def main():
    ## Cursos mongo
    dbMongo = MongoDB('localhost', 27017, 'test', 'tweets')
    collection = dbMongo.getMongoCollection()

    ## Cursor psql
    dbPg = PgDB('localhost', 'sgbdtest', 'postgres', 'docker')
    cursor = dbPg.getPgCursor()

    data_countys = dbPg.getJoinedData(cursor) ## descargamos todos los registros joineados ya que son pocos, para evitar carga en db,  tupla (country name, city name, code2)
    #applyCountryRule(collection, data_countys) ## primer etapa de filtrado
    applyStateRule(collection, data_countys) ## segunda etapa de filtrado



if __name__ == "__main__":
    main()