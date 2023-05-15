from fastapi import FastAPI
import pandas as pd
import numpy as np

df = pd.read_csv("data_def_movies.csv")

app = FastAPI()

@app.get('/peliculas_mes/{mes}')
def peliculas_mes(mes):
    '''Determina la cantidad de películas que se estrenaron en el mes dado'''
    
    peliculas_mes = df['id'][df['release_month'] == mes].count()
    return {'mes': mes, 'cantidad': int(peliculas_mes)}

@app.get('/peliculas_dia/{dia}')
def peliculas_dia(dia):
    '''Determina la cantidad de películas que se estrenaron en el día dado'''
    
    peliculas_dia = df['id'][df['release_day'] == dia].count()
    return {'dia': dia, 'cantidad': int(peliculas_dia)}

@app.get('/franquicia/{franquicia}')
def franquicia(franquicia):
    '''Determina la cantidad de películas que pertenecen a la franquicia dada, la ganancia total y la ganancia promedio'''
    
    cantidad_peliculas = df['id'][df['belongs_to_collection'] == franquicia].count()
    ganancia_total = np.sum(df['return'][df['belongs_to_collection'] == franquicia])
    ganancia_promedio = np.mean(df['return'][df['belongs_to_collection'] == franquicia])
    return {'franquicia': franquicia, 'cantidad': int(cantidad_peliculas), 'ganancia_total': ganancia_total, 'ganancia_promedio': ganancia_promedio}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais):
    '''Determina la cantidad de películas producidas en el país dado'''

    cantidad_peliculas = 0
    n = df['production_countries'].size
    for i in range(n):
        if pais in df.iloc[i, 8]:
            cantidad_peliculas += 1
    return {'pais': pais, 'cantidad': int(cantidad_peliculas)}

@app.get('/productoras/{productora}')
def productoras(productora):
    '''Determina la ganancia total y la cantidad de películas de la productora dada'''

    ganancia_total = 0
    cantidad_peliculas = 0
    n = df['production_companies'].size
    for i in range(n):
        if productora in df.iloc[i, 7]:
            ganancia_total += df.iloc[i, 20]
            cantidad_peliculas += 1
    return {'productora': productora, 'ganancia_total': ganancia_total, 'cantidad': int(cantidad_peliculas)}

@app.get('/retorno/{pelicula}')
def retorno(pelicula):
    '''Determina la inversion, la ganancia, el retorno de inversión y el año en el que se lanzo la pelicula dada'''

    inversion = 0
    ganancia = 0
    retorno = 0
    anio = 0
    n = df['title'].size
    for i in range(n):
        if df.iloc[i, 15] == pelicula:
            inversion += df.iloc[i, 1]
            ganancia += df.iloc[i, 10]
            retorno += df.iloc[i, 20]
            anio = df.iloc[i, 17]
    return {'pelicula':pelicula, 'inversion': inversion, 'ganacia': ganancia,'retorno': retorno, 'anio': int(anio)}

# ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo):
    '''Recomienda las películas similares a la película dada'''
    
    peliculas_recomendadas = []
    indice = df[df['title'] == titulo].index[0]
    popularidad = df.iloc[indice, 6]
    voto_promedio = df.iloc[indice, 16]
    anio = df.iloc[indice, 17]
    genero = df.iloc[indice, 2]
    n_genero = len(genero)
    n = df['title'].size

    for i in range(n):
        for j in range(n_genero):
            if genero[j] in df.iloc[i, 2]:
                if df.iloc[i, 15] != titulo and df.iloc[i, 15] not in peliculas_recomendadas:
                    if df.iloc[i, 6] >= popularidad and df.iloc[i, 16] >= voto_promedio and df.iloc[i, 17] == anio:
                        peliculas_recomendadas.append(df.iloc[i, 15])
    return peliculas_recomendadas