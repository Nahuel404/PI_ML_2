from fastapi import FastAPI
from starlette import responses
from typing import Optional
import pandas as pd



app = FastAPI()



@app.get('/')
def home():
    from lib import leer_html
    
    html = leer_html('home.html')
    return responses.HTMLResponse(content=html, status_code=200)



@app.get('/get_max_duratio/{year}/{platform}/{duration_type}')
def get_max_duration(
                    year: Optional[int]=None, 
                    platform: Optional[str]=None, 
                    duration_type: Optional[str]='min'
                    ):
    if(
        year<1920 
        or year>2021 
        or platform not in ['amazon','disney','hulu','netflix'] 
        or duration_type not in ['min', 'season']
        ):
        
        return ValueError('Parametros Equivocados')
    
    df_plataformas=pd.read_csv('../datasets/def_datasets/plataformas_ucompleto.csv')

    mask = (df_plataformas['duration_type']== duration_type) & (df_plataformas['platform']==platform) & (df_plataformas['release_year'] == year)

    df_aux=df_plataformas[mask]
    max=df_aux['duration_int'].max()
    mask2=df_aux['duration_int']==max
    df_aux=df_aux[mask2]
    
    name=df_aux['title']
    
    retornar={
        'pelicula': name
    }
    return retornar



@app.get('/get_score_count/{platform}/{scored}/{release_year}')
def get_score_count(
                    platform, 
                    scored: Optional[float]=None, 
                    release_year: Optional[int]=None
                    ):
    

    if (
        release_year < 1920 
        or release_year > 2021 
        or platform not in ['amazon', 'disney', 'hulu', 'netflix'] 
        or scored > 99 
        or scored < 0
    ):
        raise ValueError('Parametros equivocados')
    
    df_score = pd.read_csv('../datasets/def_datasets/plataformas_completo.csv')

    mask = (df_score['release_year'] == release_year) & (df_score['score_promedio'] > scored) & (df_score['platform'] == platform) & (df_score.type == 'movie')

    df_aux = df_score[mask]

    cantidad=len(df_aux['movieId'].drop_duplicates().index)
    respuesta={
        'plataforma': platform,
        'anio': release_year,
        'cantidad': cantidad,
        'score': scored
}
    return respuesta



@app.get('/get_count_platform/{platform}')
def get_count_platform(platform):
    
    if platform not in ['amazon', 'disney', 'hulu', 'netflix']:
        
        return ValueError('Parametro equivocado')

    df_score = pd.read_csv('../datasets/def_datasets/plataformas_completo.csv')

    mask = (df_score['type']== 'movie') & (df_score['platform']==platform)

    df_aux=df_score[mask]

    cantidad=len(df_aux['movieId'].drop_duplicates().index)

    respuesta = {
        'plataforma': platform,
        'peliculas': cantidad
    }
    return respuesta



@app.get('/get_actor/{platform}/{year}')
def get_actor(
            platform,
            year
                ):
    year=int(year)
    
    if (
        year<1920
        or year>2021
        or platform not in ['amazon', 'disney', 'hulu', 'netflix']
    ):
        return ValueError('Parametros equivocados')
    

    df_score = pd.read_csv('../datasets/def_datasets/plataformas_completo.csv')
    mask = (df_score['platform']==platform) & (df_score['release_year']==year) & (df_score['cast'] != 'unknown')
    df_aux = df_score[mask]
    df_aux['movieId'].drop_duplicates(inplace=True)
    df_aux = df_aux['cast']
    cast= df_aux.str.split(',').explode()
    cant=cast.value_counts()

    maximo = max(cant.items(), key=lambda x: x[1])
    respuesta={
        'plataforma': platform,
        'anio': year,
        'actor': maximo[0],
        'apariciones': maximo[1]}
    
    return respuesta


@app.get('/prod_per_county/{tipo}/{pais}/{year}')
def prod_per_county(
                    tipo: str,
                    pais: str,
                    year: int
                        ):
    
    df_score = pd.read_csv('../datasets/def_datasets/plataformas_completo.csv')

    if (
        year < 1920 or 
        year > 2021 or
        tipo not in ['movie', 'tv show']
        ):
        return ValueError('Parametros Equivocados')

    tipo = 'tv show'
    pais = 'spain'
    df_aux=df_score.dropna()
    df_aux = df_aux.loc[df_aux['country'].str.contains(pais)]
    df_aux = df_aux[df_aux['release_year']==year]

    respuesta=df_aux['type'].value_counts().to_dict()

    respuesta[tipo]
    respuesta2={
    'pais': pais,
    'anio': year,
    'contenido': (tipo, respuesta[tipo])
    }

    return respuesta2


@app.get('/get_recomendation/{title}')
def get_recomendation(title,):
    
    df_score = pd.read_csv('../datasets/def_datasets/plataformas_completo.csv')
    
    mask=df_score['rating'] == title
    df_aux=df_score[mask]
    cantidad=len(df_aux['movieId'].drop_duplicates().index)
    cantidad
    

    return {'recomendacion':cantidad}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)