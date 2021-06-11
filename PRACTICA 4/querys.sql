-- EJERCICIO 1
-- Seleccionar los id y el texto de 10 documentos
db.tweets.find({}, {id:1, text:1}).limit(10)

-- Seleccionar los lenguajes distintos de los tweets
db.tweets.distinct("lang")

-- Seleecionar el id, nombre, descripción y cantidad de followers de aquellos usuarios que tengan más de 100000 followers
db.tweets.find({"user.followers_count": {$gt:100000}}, {id: 1, "user.id":1,"user.name":1, "user.description":1, "user.followers_count":1})

-- Seleecionar el id, nombre y cantidad de followers de los 10 usuarios con más followers ordenado de manera descendente
db.tweets.find({}, {"user.id":1,"user.name":1, "user.followers_count":1}).sort({"user.followers_count":-1}).limit(10)


-- EJERCICIO 2
-- En base al campo "source" determinar la cantidad de usuarios que hay por cada canal
var map = function() { emit(this.source, 1);};
var countFunction = function(key, values) {
    var sum = 0;
    for(var i in values) sum += values[i];
    return sum;    
}

db.tweets.mapReduce(map, countFunction, { out: "total_por_source" });
db.total_por_source.find();



-- Determinar cantidad de tweets por cada lenguaje
var map = function() { emit(this.lang, 1);};
var countFunction = function(key, values) {
    var sum = 0;
    for(var i in values) sum += values[i];
    return sum;    
}

db.tweets.mapReduce(map, countFunction, { out: "total_por_lang" });
db.total_por_lang.find();

--Para validar: db.tweets.count({lang: "en"});


-- Agregar validación para sacar los caracteres que no son alfa numericos
-- Cantidad de tweets segun su longitud
-- Corto < 10 palabras
-- Mediano >= 10 -  < 20 palabras
-- Largo >= 20 palagras
var map = function() { 
    var words = this.text.split(" ");
    var cantidadPalabras = words.length
    var key = ""
    if (cantidadPalabras < 10) {
        key = "corto"
    } else if (cantidadPalabras < 20) {
        key = "mediano"
    } else {
        key = "largo"
    }
    emit(key, 1);};
    
var countFunction = function(key, values) {
    var sum = 0;
    for(var i in values) sum += values[i];
    return sum;    
}

db.tweets.mapReduce(map, countFunction, { out: "total_por_tipo" });
db.total_por_tipo.find();


-- EJERCICIO 3 - Usar agregación
-- Listar los 10 usuarios que publicaron más tweets, ordenarlos de manera descendente por cantidad de tweets
db.tweets.aggregate([
   { 
		$group: {
			_id: "$user.id", 
			total_tweets: {$sum: 1}
		} 
   	},
   { $out: "usuarios_con_mas_tweets" }
])

db.usuarios_con_mas_tweets.find().sort({"total_tweets":-1}).limit(10)


-- Listar por lenguaje la cantidad de followers del usuario con mayor cantidad de followers que publica en ese lenguaje
db.tweets.aggregate([
   { 
       $group: { _id: "$lang", total_followers: {$max:"$user.followers_count"}}
   },
   { $out: "lenguajes_con_mas_followers" }
])

db.lenguajes_con_mas_followers.find()
