PROYECTO INDIVIDUAL Nº1
Machine Learning Operations (MLOps)
Diosa Medina


Este readme corresponde al primer proyecto individual de la etapa de labs. En esta fase, debemos hacer un trabajo situándonos en el rol de un MLOps Engineer. Para ello hemos recibido un dataset denominado "movies_dataset.csv" con la finalidad de que lo procesemos y construyamos un modelo de recomendación en el mundo real, así como el desarrollo de una API con 7 endpoints, que debe ser deployada para que pueda estar lista para su consumo.


En este proyecto debemos seguir el ciclo de vida de un proyecto de Machine Learning, el cual debe contemplar desde el tratamiento y recolección de los datos (Ingeniería de Datos), realizando el ETL correspondiente, para luego realizar el EDA analizando un poco los datos respecto al problema a resolver (Análisis de Datos), hasta el entrenamiento y mantenimiento del modelo de ML para nuevos datos (Ciencia de Datos).


El rol a desarrollar como Data Scientist, trabajador en una start-up que provee servicios de agregación de plataformas de streaming, lo simulamos con este proyecto creando nuestro primer modelo de ML para solucionar un problema de negocio: un sistema de recomendación de películas que aún no ha sido puesto en marcha.


Nuestra mayor sorpresa fue cuando vimos los datos y nos dimos cuenta que la madurez de los mismos era poca (o nula): Datos anidados, sin transformar, sin procesos automatizados para la actualización de nuevas películas o series, entre otras cosas, haciendo nuestro trabajo imposible. Debimos empezar desde cero, probando varias métodos para acceder a los datos, métodos que no funcionaban en nuestros datos, pues aunque su formato parecía JSON, no lo era, ya tenía unas comillas simples en lugar de dobles con lo que los métodos para leer datos JSON no funcionaban. En vista de esto, procedimos a cambiar comillas simples por dobles para poder aplicar el método json, y encontrar después que se perdían 1323 datos en la columna "belongs_to_collection" por tener un None en el campo "backdrop_path", con lo que tuve que sustituirlo por un string vacío. Continuando con la normalización para convertirlos en una tabla plana, eliminar campos innecesarios y sustituir nulos, etc. Quería hacer un trabajo rápido de Data Engineer y tener un MVP (Minimum Viable Product) para la próxima semana! Pero que no salía nada rápido porque cada vez se encontraban más problemas con los datos que obligaban a regresar a las funciones de lectura de datos y modificarlas, hasta que a ultima hora encontré un método que me facilitó la lectura de los mismos, ya que no se utiliza nada de lo que he mencionado, pero por razones de tiempo cambié sólo dos de ellas, las dos primeras, después pienso cambiarlas todas.


Para las transformaciones de los datos para este MVP, solo hemos realizado las transformaciones propuestas para este proyecto, como sustituir los valores nulos de los campos "revenue", "budget" y otros campos numéricos por 0; eliminar los valores nulos del campo "release_date". Para las fechas, hemos considerado el formato AAAA-mm-dd, además creamos las columnas "release_year",  "release_month" y "release_day", en donde se extraen el año, el mes y el día de la fecha de estreno. Creamos también la columna con el retorno de inversión, llamada "return" con los campos revenue y budget, dividiendo estas dos últimas: return = revenue/budget, sustituyendo por cero los casos infinito y Nan, que resultan cuando no hay datos disponibles para calcularlo. Eliminamos las columnas que no serán utilizadas, "video", "imdb_id", "adult", "original_title", "vote_count", "poster_path" y "homepage". Adicionalmente los datos nulos de los campos categóricos los sustituí por "No collection" para el campo "belongs_to_collection", "No Genres" para el campo "genres", "No language" para el campo "original_language", "No overview" para el campo "overview", "No company" para el campo "production_company", "No country" para el campo "procuction_country", "No language" para el campo "spoken_language", "No tagline" para el campo "tagline" y "No title" para el campo "title"


Para el Desarrollo de la API, disponibilizamos los datos de la empresa usando el framework FastAPI. Las consultas propuestas fueron las siguientes:  Crear 6 funciones para los endpoints que se consumimen en la API, con un decorador por cada una (@app.get(‘/’)), quedando de la siguiente manera:

@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes):
    '''Determina la cantidad de películas que se estrenaron en el mes dado'''
    
@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia):
    '''Determina la cantidad de películas que se estrenaron en el día dado'''
    
@app.get('/franquicia/{franquicia}')
def franquicia(franquicia):
    '''Determina la cantidad de películas que pertenecen a la franquicia dada, la ganancia total y la ganancia promedio'''

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais):
    '''Determina la cantidad de películas producidas en el país dado'''

@app.get('/productoras/{productora}')
def productoras(productora):
    '''Determina la ganancia total y la cantidad de películas de la productora dada'''

@app.get('/retorno/{pelicula}')
def retorno(pelicula):
    '''Determina la inversion, la ganancia, el retorno de inversión y el año en el que se lanzo la pelicula dada'''


Para el Análisis exploratorio de los datos: (Exploratory Data Analysis-EDA), una vez que limpiamos los datos, investigamos las relaciones entre las variables del dataset dado, encontrando que hay outliers que hacen que la mayoría de las distribuciones sean asimétricas positivas, a excepción del "vote_average que de no ser por los valores 0, que no son resultantes de valores nulos, tendría una distribución aproximadamente simétrica tendiendo a una distribución normal. Además no existe correlaciones significativas entre las variables a excepción de las variables budge y revenue; considerando que no vale la pena explorar un análisis de asociación entre estas variables numéricas, más aún considerando el problema de negocio en mente, el sistema de recomendación de películas, en donde las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos (campo "title"), en el resumen (campo "overview")



Ahora que la data es consumible por la API, que está lista para consumirse por los departamentos de Analytics y Machine Learning, y nuestro EDA nos permite entender bien los datos a los que tenemos acceso, entrenamos nuestro modelo de machine learning para armar un sistema de recomendación de películas, que recomiende películas a los usuarios basándose en películas similares, encontrando la similitud de puntuación entre esa película y el resto de películas, ordenándolas según el score de similaridad y devolviendo una lista de Python con 5 valores, cada uno siendo el string del nombre de las películas con mayor puntaje, en orden descendente. Este sistema de recomendación será deployado como la última función de la API anterior y se llama:

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    '''Recomienda las películas similares a la película dada'''