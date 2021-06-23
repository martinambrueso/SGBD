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
                            upper(co.code) as c_pais
                        FROM 
                            city c
                        JOIN 
                            country co
                        ON 
                            co.code = c.countrycode;
                    """
                )

        return cur.fetchall()


def generarMapa(dbPg):
    mapaPaises = {}
    for pais,ciudad,distrito,c_pais in dbPg:
        if ciudad.lower() not in mapaPaises:
            mapaPaises[ciudad.lower()] = c_pais
        if distrito.lower() not in mapaPaises:
            mapaPaises[distrito.lower()] = c_pais
        if pais.lower() not in mapaPaises:
            mapaPaises[pais.lower()] = c_pais
    mapaPaises["spain"] = "ESP"
    return mapaPaises

def applyStateRule(collection, mapaPaises): ## HACER REFACTORING URGENTE DESPUES DE QUE FUNQUE
    dataResult = collection.find({'real_location': {'$exists':False}}) ## se toma remanente en aquellos documentos que no tiene presente el nuevo campo real_location

    for element in dataResult:
        update = False
        userLocation = str(element['user']['location']).lower()
        result = re.split('[,/-]', userLocation) # spliteamos las palabras
        for e in result:
            #print(e)
            if e in mapaPaises:
                res = mapaPaises[e]
                collection.update_one({'id': element['id']}, {'$set': {'real_location': res}})
                update = True
                break
        if not update and userLocation.replace(" ", "") in mapaPaises: #Si no se actualiza con el for de antes, proobamos sacando los espacios ya que hay casos de ' Argentina'
            res = mapaPaises[userLocation.replace(" ", "")]
            collection.update_one({'id': element['id']}, {'$set': {'real_location': res}})
            update = True

        if not update:
            print(userLocation)
            
def main():
    ## Cursos mongo
    dbMongo = MongoDB('localhost', 27017, 'test', 'tweets')
    collection = dbMongo.getMongoCollection()

    ## Cursor psql
    dbPg = PgDB('localhost', 'world', 'postgres', 'admin')
    cursor = dbPg.getPgCursor()

    data_countys = dbPg.getJoinedData(cursor) ## descargamos todos los registros joineados ya que son pocos, para evitar carga en db,  tupla (country name, city name, code2)
    mapaPaises = generarMapa(data_countys)
    applyStateRule(collection, mapaPaises) ## segunda etapa de filtrado



if __name__ == "__main__":
    main()