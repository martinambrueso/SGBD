-- Población de Argentina
select population from country where name = 'Argentina';

-- Todos los continentes sin repetir
select distinct(continent) from country;

-- Nombres de los paıses de America del Sur con mas de 15 millones de habitantes
select name from country where continent = 'South America' and population > 15000000;

-- Nombre y producto bruto de los diez pa ıses con mayor producto bruto (gnp)
select name, gnp from country order by gnp desc limit 10;

-- Forma de gobierno y cantidad de paises con dicha forma de gobierno ordenados por cantidad de modo descentente
select governmentform, count(name) as cantidad_de_paises from country group by governmentform order by cantidad_de_paises desc;

-- Los nombres de los continentes con sus respectivas superficies ordenados de forma descendentes por superficie
select continent, sum(surfacearea) as superficie from country group by continent order by superficie desc;

-- Los continentes y la cantidad de paises que los componen de aquellos continentes con mas de 15 paıses
select continent, count(name) as cantidad_de_paises from country group by continent HAVING count(name) > 15 order by cantidad_de_paises desc;

-- Idem punto anterior pero que los pa ́ıses que se tengan en cuenta tengan una poblacion de mas de 20 millones de personas
select continent, count(name) as cantidad_de_paises from country where population > 20000000 group by continent HAVING count(name) > 15 order by cantidad_de_paises desc;


-- Subqueries

-- Nombre del pais y expectativa de vida de los paises con mayor y menor expectativa de vida
select name, lifeexpectancy from country 
where lifeexpectancy = (select min(lifeexpectancy) from country) or lifeexpectancy = (select max(lifeexpectancy) from country);

-- Nombre de los paises y año de independencia que pertenecen al coninente del paìs que se independizo hace más tiempo
select name, indepyear from country
where continent = (select continent from country where indepyear = (select min(indepyear) from country));


-- Nomber de los continentes que no pertenecen al conjunto de los continentes más pobres



-- Joins
-- Paises y lenguas de los paises de Oceania
select cy.name, cl.language from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
where cy.continent = 'Oceania';

-- Los Paises y la cantidad de lenguas de los que se habla más de una lengua. Ordenado de forma descendente
select cy.name, count(cl.language) as cantidad_de_lenguas from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
where cy.continent = 'Oceania'
group by cy.name
having count(Distinct(cl.language)) > 1
order by cantidad_de_lenguas desc;


-- Lenguas que se hablan en el continente más pobre, sin contar antarctica
select continent, sum(gnp) as total_gnp from country where continent != 'Antarctica' group by continent order by total_gnp asc limit 1;

select cl.language from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
where cy.continent = 'Oceania';


-- Nombre de los paises y sus respectivas poblaciones calculados segun:
-- Tabla country
select name, population from country;

-- Suma de las poblaciones segun la tabla city y calcular el porcentaje de la población urbana y ordenar por porcentaje descendente
-- Como se sabe la ciudad si es urbana o no?
select cy.name, sum(ct.population) as poblacion, 
(sum(ct.population) * 100) / sum(cy.population) as porcentaje
from country cy
inner join city ct on ct.countrycode = cy.code
group by cy.name order by porcentaje desc;



Analizar los scripts de creacion de las tres tablas (country, city, countrylanguage) y responder a las siguientes preguntas:
Cual es la clave primaria (primary key) de cada tabla?
country - code
countrylanguage - countrycode, language
city - id

Cuales son las claves foraneas (foreign key) de cada tabla?
country - capital
countrylanguage - countrycode
city -  no tiene

A tu criterio, falta alguna clave foranea?
Como criterio tomo las definiciones del constraint sql en la definicion ddl. No falta ninguna clave, ya que las relaciones  se establecen solo 
desde countrylanguage > country, country > city, no se detalla acerca de mas relaciones (countrylanguage > city).

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



INSERT INTO public.stats
select cy.code, count(cl.language), sum(cy.population) from country cy
inner join countrylanguage cl on cl.countrycode = cy.code
where cy.continent = 'Oceania'
group by cy.code;
