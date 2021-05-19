-- Población de Argentina
select population from country where name = 'Argentina';

-- Todos los continentes sin repetir
select distinct(continent) from country;

-- Nombres de los paıses de America del Sur con mas de 15 millones de habitantes
select name from country where continent = 'South America' and population > 15000000;

-- Nombre y producto bruto de los diez pa ıses con mayor producto bruto (gnp)
select name, gnp from country order by gnp desc limit 10;

-- Forma de gobierno y cantidad de paises con dicha forma de gobierno ordenados por cantidad de modo descentente
select governmentform, count(name) as cantidad_de_paises from country 
group by governmentform order by cantidad_de_paises desc;

-- Los nombres de los continentes con sus respectivas superficies ordenados de forma descendentes por superficie
select continent, sum(surfacearea) as superficie from country group by continent order by superficie desc;

-- Los continentes y la cantidad de paises que los componen de aquellos continentes con mas de 15 paıses
select continent, count(name) as cantidad_de_paises from country 
group by continent HAVING count(name) > 15 order by cantidad_de_paises desc;

-- Idem punto anterior pero que los pa ́ıses que se tengan en cuenta tengan una poblacion de mas de 20 millones de personas
select continent, count(name) as cantidad_de_paises 
from country where population > 20000000 group by continent HAVING count(name) > 15 order by cantidad_de_paises desc;


-- Subqueries

-- Nombre del pais y expectativa de vida de los paises con mayor y menor expectativa de vida
select name, lifeexpectancy from country 
where lifeexpectancy = (select min(lifeexpectancy) from country) 
or lifeexpectancy = (select max(lifeexpectancy) from country);

-- Nombre de los paises y año de independencia que pertenecen al coninente del paìs que se independizo hace más tiempo
select name, indepyear from country
where continent = (select continent from country where indepyear = (select min(indepyear) from country));


-- Nomber de los continentes que no pertenecen al conjunto de los continentes más pobres
select distinct(cy.continent) from country cy 
join (select continent, avg(gnp) as gnp_promedio from country group by continent order by gnp_promedio desc limit 4)
 sub_country on sub_country.continent = cy.continent;

-- Joins
-- Paises y lenguas de los paises de Oceania
select cy.name, cl.language from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
where cy.continent = 'Oceania';

-- Los Paises y la cantidad de lenguas de los que se habla más de una lengua. Ordenado de forma descendente
select cy.name, count(cl.language) as cantidad_de_lenguas from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
group by cy.name
having count(cl.language) > 1
order by cantidad_de_lenguas desc;

-- Lenguas que se hablan en el continente más pobre, sin contar antarctica
-- avg de gnp 
select distinct(cl.language) as cantidad_de_lenguas from country cy 
join (select continent, avg(gnp) as gnp_promedio from country 
      where continent != 'Antarctica' group by continent order by gnp_promedio asc limit 1)
 sub_country on sub_country.continent = cy.continent
 inner join countrylanguage cl on cl.countrycode = cy.code;


-- Nombre de los paises y sus respectivas poblaciones calculados segun:
-- Tabla country
select name, population from country;

-- Suma de las poblaciones segun la tabla city y calcular el porcentaje de la población urbana y ordenar por porcentaje descendente
select cy.name, sum(ct.population) as poblacion, 
(sum(ct.population) * 100) / sum(cy.population) as porcentaje
from country cy
inner join city ct on ct.countrycode = cy.code
group by cy.name order by porcentaje desc;

-- Analizar los scripts de creacion de las tres tablas (country, city, countrylanguage) y responder a las siguientes preguntas:
-- Cual es la clave primaria (primary key) de cada tabla?
-- country - code
-- countrylanguage - countrycode, language
-- city - id

-- Cuales son las claves foraneas (foreign key) de cada tabla?
-- country - capital
-- countrylanguage - countrycode
-- city -  no tiene

-- A tu criterio, falta alguna clave foranea?
-- Como criterio tomo las definiciones del constraint sql en la definicion ddl. No falta ninguna clave, ya que las relaciones  se establecen solo 
-- desde countrylanguage > country, country > city, no se detalla acerca de mas relaciones (countrylanguage > city).

-- Table: public.stats

-- DROP TABLE public.stats;

CREATE TABLE public.stats
(
    countrycode character(4) COLLATE pg_catalog."default" NOT NULL,
    cant_lenguas numeric NOT NULL,
    pop_urbana numeric NOT NULL,
    CONSTRAINT stats_pkey PRIMARY KEY (countrycode),
    CONSTRAINT countrycode FOREIGN KEY (countrycode)
        REFERENCES public.country (code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE public.stats
    OWNER to postgres;

select * from stats;

-- se inserta la cantidad de lenguas
INSERT INTO public.stats
select cy.code, count(cl.language), 0 from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
group by cy.code;

-- se hace el update para la cantidad de población del as ciudades
update public.stats st
set pop_urbana = sub.total_population
from (
select cy.code, sum(ct.population) as total_population
from country cy
inner join city ct on ct.countrycode = cy.code
group by cy.code 
) sub where st.countrycode = sub.code;




-- Tabla sitio
CREATE TABLE public.sitio
(
    id bigint NOT NULL,
    entidad varchar NULL,
    tipo_entidad varchar NULL,
	pais varchar NULL,
	countrycode character(4) NULL,
    CONSTRAINT sitio_pkey PRIMARY KEY (id),
    CONSTRAINT countrycode FOREIGN KEY (countrycode)
        REFERENCES public.country (code) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)



-- Ejercicio 5
select * from sitio s1, sitio s2 where 
s1.countrycode = s2.countrycode
and s1.entidad like 'a%' and s2.entidad like 'b%'
limit 100;

EXPLAIN select * from sitio s1, sitio s2 where 
s1.countrycode = s2.countrycode
and s1.entidad like 'a%' and s2.entidad like 'b%'
limit 100;

CREATE INDEX sitio_countrycode_idx
ON sitio (countrycode);

EXPLAIN select * from sitio s1, sitio s2 where 
s1.countrycode = s2.countrycode
and s1.entidad like 'a%' and s2.entidad like 'b%'
limit 100;

-- SIN INDICE

--Limit  (cost=1000.00..3848.75 rows=100 width=70)--
--  ->  Nested Loop  (cost=1000.00..55225874.77 rows=1938562 width=70)--
--        Join Filter: (s1.countrycode = s2.countrycode)--
--        ->  Seq Scan on sitio s1  (cost=0.00..19351.64 rows=60656 width=35)--
--              Filter: ((entidad)::text ~~ 'a%'::text)--
--        ->  Materialize  (cost=1000.00..19419.73 rows=60656 width=35)--
--              ->  Gather  (cost=1000.00..19116.45 rows=60656 width=35)--
--                    Workers Planned: 2--
--                    ->  Parallel Seq Scan on sitio s2  (cost=0.00..12050.85 rows=25273 width=35)--
--                          Filter: ((entidad)::text ~~ 'b%'::text)--



-- CON INDICE

--Limit  (cost=0.85..7.34 rows=100 width=70)--
--  ->  Merge Join  (cost=0.85..125562.25 rows=1933707 width=70)--
--        Merge Cond: (s1.countrycode = s2.countrycode)--
--        ->  Index Scan using sitio_countrycode_idx on sitio s1  (cost=0.42..48202.60 rows=60580 width=35)--
--              Filter: ((entidad)::text ~~ 'a%'::text)--
--        ->  Materialize  (cost=0.42..48354.05 rows=60580 width=35)--
--              ->  Index Scan using sitio_countrycode_idx on sitio s2  (cost=0.42..48202.60 rows=60580 width=35)--
--                    Filter: ((entidad)::text ~~ 'b%'::text)--


-- COMO RESULTADO DE LAS EJECUCIONES, PODEMOS VER QUE LA ULTILIZACION DE INDICES RESTA COSTOS
-- DE OPERACIONES ADICIONALES, RESPECTO DE LA EJECUCION SIN INDICES. TAMBIEN, PODEMOS VER QUE
-- LA QUERY EJECUTADA SIN INDICE SE EJECUTA EN DOS TRABAJOS, DE LO CONTRARIO, CON INDICE SOLO UNO.
-- EL ARBOL DE EJECUCION, FINALMENTE, QUEDA CON MENOS JOBS, POR LO TANTO, MENOS COSTOS.