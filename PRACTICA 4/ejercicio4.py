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
        if item[position] != None and elem != None and len(re.findall(item[position], (elem.lower()).strip())) != 0:
            return item
            break



def applyRule(collection, condition, projection, data, position):
    dataResult = collection.find(condition, projection)

    for element in dataResult:
        result = re.split('[,/-]', str(element['user']['location'])) # spliteamos las palabras
        for e in result:
            res = find(data, e, position) ## tercer parametro es de posicion de la tupla resultante de la consulta sql
            if res:
                collection.update_one({'id': element['id']}, {'$set': {'real_location': ((res[position]).lower()).strip()}})
                break



def main():
    ## Cursos mongo
    dbMongo = MongoDB('localhost', 27017, 'test', 'tweets')
    collection = dbMongo.getMongoCollection()

    ## Cursor psql
    dbPg = PgDB('localhost', 'sgbdtest', 'postgres', 'docker')
    cursor = dbPg.getPgCursor()

    data_countys = dbPg.getJoinedData(cursor) ## descargamos todos los registros joineados ya que son pocos, para evitar carga en db,  tupla (country name, city name, code2)
    
    ## applyRule (collection, filterQuery, projectionQuery, tuplaResultSQL, pisicion_tupla(pais, cuidad, distrito, c_pais))
    applyRule(collection, None, {"id": 1,"user.location": 1}, data_countys, 0)
    applyRule(collection, {'real_location': {'$exists':False}}, None, data_countys, 1)
    applyRule(collection, {'real_location': {'$exists':False}}, {}, data_countys, 3)



if __name__ == "__main__":
    main()



## AGREGAR CASO NULL Y Ciudad Autónoma de Buenos Aire
## > db.tweets.find({'user.location': null},{}).count()   48169
## una capa mas podria ser regla por codigo - Houston, TX
## New York, USA