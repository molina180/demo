import dash
from dash import dcc, html, callback
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from pysentimiento import create_analyzer
import json
import spacy
from collections import Counter
from wordcloud import WordCloud
from collections import defaultdict
from nltk.corpus import stopwords
import nltk
import base64
import io
import squarify
import os

nltk.download('stopwords')

# Modificar algunos parámetros del esquema de color
modified_colorscale = [
    [0.0, '#312d3f'],
    [0.05, '#364253'],
    [0.1, '#3e4157'],
    [0.15, '#47546c'],
    [0.2, '#4e5270'],
    [0.25, '#556485'],
    [0.3, '#5d6a9b'],
    [0.35, '#636588'],
    [0.4, '#6b6e9e'],
    [0.45, '#7272b3'],
    [0.5, '#7f7e9d'],
    [0.55, '#8892b2'],
    [0.6, '#92a7c7'],
    [0.65, '#9d94ae'],
    [0.7, '#a9abc4'],
    [0.75, '#b8adc0'],
    [0.8, '#c6c1d6'],
    [0.85, '#d2c7d2'],
    [0.9, '#dfd4e8'],
    [0.95, '#eae5e6'],
    [1.0, '#ffffff']
]

# Inicializar modelo de spaCy para procesamiento de texto
nlp = spacy.load('es_core_news_sm')

# Función para obtener sustantivos y adjetivos
def obtener_sustantivos_y_adjetivos(texto):
    doc = nlp(texto)

    # Pronombres relativos y preposiciones adicionales a eliminar
    palabras_a_eliminar = set(['el', 'la', 'los', 'las', 'un', 'una', 'nos' ,'unos', 'unas', 'este', 'esta', 'estos', 'estas',
                               'que', 'cómo', 'para', 'lo' ,'los', 'que', 'de', 'con', 'esto', 'su', 'sus', 'otro', 'y', 'su',
                               'ese', 'esta', 'esos', 'estas', 'a', 'mi', 'por', 'al', 'del', 'se', 'es', 'le', 'les', 'va','si', 'en'])

    # Agregar pronombres relativos y preposiciones a eliminar
    palabras_a_eliminar |= set(['quién', 'quienes', 'cuyo', 'cuya', 'cuando', 'donde', 'como', 'sobre', 'entre', 'hacia', 
                                'desde', 'aunque', 'sin', 'hasta', 'tras', 'durante', 'mediante', 'contra', 'bajo', 'sobre', 
                                'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'hacia', 'hasta', 
                                'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras', 'versus'])

    sustantivos = [token.text for token in doc if token.pos_ == 'NOUN' and token.text.lower() not in palabras_a_eliminar]
    adjetivos = [token.text for token in doc if token.pos_ == 'ADJ' and token.text.lower() not in palabras_a_eliminar]

    sustantivos_frecuentes = Counter(sustantivos).most_common(10)
    adjetivos_frecuentes = Counter(adjetivos).most_common(10)
    
    return sustantivos_frecuentes, adjetivos_frecuentes


# Función para clasificar los sentimientos como "negativos" o "positivos"
def clasificar_sentimiento(sentimiento):
    if sentimiento in ['tristeza', 'miedo', 'enojo']:
        return 'Negativos'
    else:
        return 'Positivos'

# Crear aplicación Dash
dash.register_page(__name__, path='/dashboard', name="Dashboard 📊")

# Define los estilos CSS
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

# Obtener lista de archivos JSON en la carpeta /data
archivos_json = [archivo for archivo in os.listdir('data') if archivo.endswith('.json')]

# Generar opciones para el Dropdown con nombres legibles
archivos_dropdown_options = []
for archivo in archivos_json:
    nombre_legible = archivo.replace('_', ' ').replace('.json', '').title()  # Reemplazar guiones bajos y eliminar la extensión .json
    opcion = {'label': nombre_legible, 'value': archivo}
    archivos_dropdown_options.append(opcion)

# Definir el layout del dashboard con los estilos CSS integrados y centrar los elementos
layout = html.Div(children=[
    html.Div(
        className="container",  # Agregar clase para centrar y agregar márgenes
        children=[
            html.H1(children='Dashboard', className='text-center mt-5 mb-4'),

            # Dropdown para seleccionar el archivo JSON
            html.H6(children='Selecciona la data a analizar', className='text-left mt-5 mb-3'),
            dcc.Dropdown(
                id='json-dropdown',
                options=archivos_dropdown_options,
                value=archivos_json[0],  # Valor predeterminado: primer archivo en la lista
                clearable=False,
                className='mb-4'
            ),

            # Gráfico de dispersión
            html.H2(children='Likes y comentarios', className='text-center mt-5 mb-3'),
            dcc.Dropdown(
                id='data-dropdown',
                options=[
                    {'label': 'Likes Count', 'value': 'likesCount'},
                    {'label': 'Comments Count', 'value': 'commentsCount'}
                ],
                value='likesCount',
                clearable=False,
                className='mb-4'
            ),
            dcc.Graph(
                id='scatter-plot',
                style={'height': '50vh'},
                className='plot-container'
            ),

            # Treemap de hashtags
            html.H2(children='Hashtags utilizados', className='text-center mt-5 mb-3'),
            dcc.Loading(
                id="loading-hashtags",
                children=dcc.Graph(id='hashtag-treemap')
            ), 

            # Treemap de sustantivos
            html.H2(children='Sustantivos más utilizados', className='text-center mt-5 mb-3'),
            dcc.Loading(
                id="loading-nouns",
                children=[dcc.Graph(id='noun-treemap')]
            ),

            # Treemap de adjetivos
            html.H2(children='Adjetivos más utilizados', className='text-center mt-5 mb-3'),
            dcc.Loading(
                id="loading-adjectives",
                children=[dcc.Graph(id='adjective-treemap')]
            ),

            # Nube de palabras
            html.H2(children='Nube de palabras', className='text-center mt-5 mb-3'),
            html.Img(id='wordcloud', style={'width': '100%', 'height': 'auto'}
            ),

            # Gráfico de pastel de distribución de sentimientos
            html.H2(children='Distribución de Sentimientos', className='text-center mt-5 mb-3'),
            dcc.Loading(
                id="loading-sentiment-piechart",
                children=[dcc.Graph(id='sentiment-piechart')]
            ),
            
            html.H2(children='Nube de Sentimientos', className='text-center mt-5 mb-3'),
            dcc.Loading(
                id="loading-wordclouds",
                style={'width': '100%', 'height': 'auto'},
                children=[
                    dcc.Dropdown(
                        id='wordcloud-dropdown',
                        options=[
                            {'label': 'Negativas', 'value': 'NEG'},
                            {'label': 'Positivas', 'value': 'POS'},
                            {'label': 'Neutrales', 'value': 'NEU'}
                        ],
                        value='POS',
                        clearable=False,
                        className='mb-4',
                        style={'width': '50%', 'margin': '20px', 'display': 'block'}
                    ),
                    html.Div([
                        html.Img(id='wordclouds', style={'width': '100%', 'height': 'auto'})
                    ], id='wordclouds-container', style={'width': '100%', 'height': 'auto', 'margin': '0 auto'})
                ]
            ),

            # # Gráfico Sunburst
            # html.H2(children='Distribución de emociones', className='text-center mt-5 mb-3'),
            # dcc.Loading(
            #     id="loading-sunburst-chart",
            #     children=[dcc.Graph(id='sunburst-chart')]
            # ),
        ]
    ),

    # Estilos CSS
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'
    )
])


# Callback para actualizar el gráfico de dispersión
@callback(
    dash.dependencies.Output('scatter-plot', 'figure'),
    [dash.dependencies.Input('json-dropdown', 'value'),
     dash.dependencies.Input('data-dropdown', 'value')],
)

def update_scatter_plot(selected_json, selected_data):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    df = pd.DataFrame(data)
    fig = px.scatter(df, x='timestamp', y=selected_data, color_discrete_sequence=['#47546c'])
    #fig.add_trace(go.Scatter(x=df['timestamp'], y=df[selected_data], mode='lines', line=dict(color='#a9abc4'), name=None))
    fig.update_layout(title=f'Gráfico de dispersión ({selected_data})', showlegend=False, title_x=0.05, title_y=0.95)
    return fig


# Callback para actualizar el treemap de hashtags
@callback(
    dash.dependencies.Output('hashtag-treemap', 'figure'),
    [dash.dependencies.Input('json-dropdown', 'value')]
)

def update_hashtag_treemap(selected_json):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    df_hashtags = pd.DataFrame([{'Hashtag': hashtag} for d in data for hashtag in d['hashtags']])
    
    # Count the frequency of each hashtag
    hashtag_counts = df_hashtags['Hashtag'].value_counts().reset_index()
    hashtag_counts.columns = ['Hashtag', 'Frecuencia']
    top_10_hashtags = hashtag_counts.head(10)
    fig = px.treemap(top_10_hashtags, path=['Hashtag'], values='Frecuencia', color='Frecuencia',
                     color_continuous_scale=modified_colorscale)
    fig.update_layout(title='Top 10 Hashtags utilizados', title_x=0.05, title_y=0.95)

    return fig


# Callback para actualizar los treemaps de sustantivos y adjetivos
@callback(
    dash.dependencies.Output('noun-treemap', 'figure'),
    [dash.dependencies.Input('json-dropdown', 'value'),
     dash.dependencies.Input('data-dropdown', 'value')]
)

def update_noun_treemap(selected_json, selected_data):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    sustantivos, _ = obtener_sustantivos_y_adjetivos(' '.join([d['cleanText'] for d in data]))
    df_sustantivos = pd.DataFrame(sustantivos, columns=['Sustantivo', 'Frecuencia'])
    return generar_treemap(df_sustantivos, 'Sustantivo')

@callback(
    dash.dependencies.Output('adjective-treemap', 'figure'),
    [dash.dependencies.Input('json-dropdown', 'value'),
     dash.dependencies.Input('data-dropdown', 'value')]
)

def update_adjective_treemap(selected_json, selected_data):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    _, adjetivos = obtener_sustantivos_y_adjetivos(' '.join([d['cleanText'] for d in data]))
    df_adjetivos = pd.DataFrame(adjetivos, columns=['Adjetivo', 'Frecuencia'])
    df_adjetivos_sorted = df_adjetivos.sort_values(by='Frecuencia', ascending=False)
    top_10_adjetivos = df_adjetivos_sorted.head(10)
    return generar_treemap(top_10_adjetivos, 'Adjetivo')


def generar_treemap(df, label_column):
    df_sorted = df.sort_values(by='Frecuencia', ascending=False)
    top_10 = df_sorted.head(10)
    fig = px.treemap(top_10, path=[label_column], values='Frecuencia', color='Frecuencia',
                     color_continuous_scale=modified_colorscale, labels={'Frecuencia': 'Frecuencia'},
                     hover_data=[label_column, 'Frecuencia'])
    fig.update_traces(textinfo='label+value')
    fig.update_layout(title=f'Los 10 {label_column}s más utilizados', title_x=0.05, title_y=0.95)
    return fig

# Generar la nube de palabras
def generar_nube_palabras(texto):
    stop_words = set(stopwords.words('spanish'))
    # Pronombres relativos y preposiciones adicionales a eliminar
    palabras_a_eliminar = set(['el', 'la', 'los', 'las', 'un', 'una', 'nos' ,'unos', 'unas', 'este', 'esta', 'estos', 'estas',
                               'que', 'cómo', 'para', 'lo' ,'los', 'que', 'de', 'con', 'esto', 'su', 'sus', 'otro', 'y', 'su',
                               'ese', 'esta', 'esos', 'estas', 'a', 'mi', 'por', 'al', 'del', 'se', 'es', 'le', 'les', 'va','si', 'en'])

    # Agregar pronombres relativos y preposiciones a eliminar
    palabras_a_eliminar |= set(['quién', 'quienes', 'cuyo', 'cuya', 'cuando', 'donde', 'como', 'sobre', 'entre', 'hacia', 
                                'desde', 'aunque', 'sin', 'hasta', 'tras', 'durante', 'mediante', 'contra', 'bajo', 'sobre', 
                                'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'en', 'entre', 'hacia', 'hasta', 
                                'para', 'por', 'según', 'sin', 'so', 'sobre', 'tras', 'versus'])

    # Texto sin palabras innecesarias
    texto_limpiado = ' '.join([palabra for palabra in texto.split() if palabra.lower() not in palabras_a_eliminar])

    # Crear la nube de palabras con parámetros ajustados
    wordcloud = WordCloud(
        width=1200,  # Aumenta el ancho de la nube de palabras
        height=600,  # Aumenta la altura de la nube de palabras
        background_color='white',
        colormap='twilight',
        stopwords = stop_words,
        contour_color='black',
        contour_width=1,
        prefer_horizontal=0.8,
        max_words=20,
        font_path='assets/Roboto.ttf',  # Utiliza una tipografía clara y legible
    ).generate(texto_limpiado)

    return wordcloud

# Función para obtener sentimientos
analyzer = create_analyzer(task="sentiment", lang="es")

def obtener_sentimiento(texto):
    resultado = analyzer.predict(texto)
    sentimiento = max(resultado.probas, key=resultado.probas.get)
    return sentimiento

# Callback para actualizar la nube de palabras
@callback(
    dash.dependencies.Output('wordcloud', 'src'),
    [dash.dependencies.Input('json-dropdown', 'value')]
)


def update_wordcloud(selected_json):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    texto_ejemplo = ' '.join([d['cleanText'] for d in data])
    wordcloud = generar_nube_palabras(texto_ejemplo)

    # Convertir la imagen a bytes
    img_bytes = io.BytesIO()
    wordcloud.to_image().save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    # Codificar la imagen en base64
    img_buffer = base64.b64encode(img_bytes.read())
    return f'data:image/png;base64,{img_buffer.decode()}'

# Callback para actualizar el gráfico de pastel de distribución de sentimientos
@callback(
    dash.dependencies.Output('sentiment-piechart', 'figure'),
    [dash.dependencies.Input('json-dropdown', 'value')]
)


def update_sentiment_piechart(selected_json):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)
    sentimientos = [obtener_sentimiento(d['cleanText']) for d in data]
    sentimientos_counts = Counter(sentimientos)
    labels = list(sentimientos_counts.keys())  # Convertir dict_keys en una lista
    values = list(sentimientos_counts.values())  # Convertir dict_values en una lista
    custom_colors = ['#47546c', '#7f7e9d', '#a9abc4']  # Puedes agregar más colores según sea necesario
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5)])
    fig.update_traces(marker=dict(colors=custom_colors))
    fig.update_layout(title='Distribución de sentimientos')
    
    return fig


# def analizar_texto_y_generar_sunburst_data(texto):
#     nlp = spacy.load("es_core_news_sm")
#     doc = nlp(texto)
    
#     # Contar la frecuencia de palabras asociadas a cada emoción
#     emociones_frecuencia = defaultdict(int)
#     emociones_presentes = set()
    
#     for token in doc:
#         for emocion, palabras_emocion in emociones_palabras_ampliado.items():
#             if token.text.lower() in palabras_emocion:
#                 emociones_frecuencia[emocion] += 1
#                 emociones_presentes.add(emocion)
    
#     # Crear una lista de diccionarios con los resultados del análisis del texto
#     datos = []
#     for emocion in emociones_presentes:
#         palabras_emocion = emociones_palabras_ampliado[emocion]
#         for token in doc:
#             if token.text.lower() in palabras_emocion:
#                 datos.append({
#                     'frecuencia': emociones_frecuencia[emocion],
#                     'palabra': token.text.lower(),
#                     'sentimiento': emocion
#             })
    
#     # Convertir la lista de diccionarios en un DataFrame
#     df = pd.DataFrame(datos)
    
#     # Clasificar los sentimientos
#     df['sentiment'] = df['sentimiento'].apply(clasificar_sentimiento)
    
#     # Ordenar el DataFrame
#     df = df.sort_values(by=['sentiment', 'sentimiento', 'palabra'])
    
#     # Convertir el DataFrame a un diccionario
#     data = defaultdict(list)
#     for _, row in df.iterrows():
#         data['frecuencia'].append(row['frecuencia'])
#         data['palabra'].append(row['palabra'])
#         data['sentimiento'].append(row['sentimiento'])
#         data['sentiment'].append(row['sentiment'])
    
#     return dict(data)

@callback(
    dash.dependencies.Output('wordclouds', 'src'),
    [dash.dependencies.Input('wordcloud-dropdown', 'value'),
     dash.dependencies.Input('json-dropdown', 'value')]
)
def update_wordcloud(selected_sentimiento, selected_json):
    with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
        data = json.load(file)

    # Crear un DataFrame con los datos
    df = pd.DataFrame(data)

    # Obtener el sentimiento para cada texto limpio
    df['sentimiento'] = df['cleanText'].apply(obtener_sentimiento)

    # Filtrar los datos según el sentimiento seleccionado
    df_sentimiento = df[df['sentimiento'] == selected_sentimiento]

    # Generar la nube de palabras para el sentimiento seleccionado
    mensajes_sentimiento = df_sentimiento['cleanText'].str.cat(sep=' ')
    if mensajes_sentimiento:
        wordcloud = generar_nube_palabras(mensajes_sentimiento)

        # Guardar la nube de palabras en la carpeta assets
        wordcloud_path = f'assets/nube_{selected_sentimiento.lower()}.png'
        wordcloud.to_file(wordcloud_path)

        # Leer la imagen en base64 para mostrarla en el frontend
        with open(wordcloud_path, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

        # Devolver la URL de la imagen
        return f'data:image/png;base64,{encoded_img}'
    else:
        # No se encontraron textos con el sentimiento seleccionado
        return '/assets/no_text_found.png'


# Callback para actualizar el gráfico Sunburst
# @callback(
#     dash.dependencies.Output('sunburst-chart', 'figure'),
#     [dash.dependencies.Input('json-dropdown', 'value')]
# )
# def update_sunburst_chart(selected_json):
#     with open(os.path.join('data', selected_json), 'r', encoding="UTF-8") as file:
#         data = json.load(file)
#     texto_limpio = ' '.join(entry['cleanText'] for entry in data)
#     sunburst_data = analizar_texto_y_generar_sunburst_data(texto_limpio)
#     color_discrete_sequence = ['#47546c', '#a9abc4']
#     fig = px.sunburst(sunburst_data, path=['sentiment', 'sentimiento', 'palabra'], values='frecuencia',
#                     color='sentiment', color_discrete_sequence=color_discrete_sequence)
#     fig.update_layout(title='Distribución de emociones', title_x=0.05, title_y=0.95)
#     return fig



