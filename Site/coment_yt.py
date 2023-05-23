import pickle
import os
import pandas as pd
from urllib.parse import urlparse, parse_qs
import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask, render_template, request, redirect, session, flash, url_for,jsonify
import toml
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

with open('config.toml', 'r') as file:
    config = toml.load(file)

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY = config['DEVELOPER_KEY']

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

#Carrega Modelo:
model = pickle.load(open("lrModel", "rb"))
vectorizer = pickle.load(open("vectorizer", "rb"))

#trata o texto e classifica o texto
from tratamento import trata
def classifica_tweet(text):
    test_vectors = vectorizer.transform(trata(text))
    return model.predict(test_vectors)

#Puxa comentarios do vídio do youtube
def get_video_comments(youtube,video_id):
    try:
        comments = []
        # Primeira solicitação para obter os comentários principais
        results = youtube.commentThreads().list(
            part='snippet',
            videoId=video_id,
            textFormat='plainText',
            maxResults=100
        ).execute()

        # Percorre todas as páginas de resultados
        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Verifica se há mais páginas de resultados
            if 'nextPageToken' in results:
                next_page_token = results['nextPageToken']
                results = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=100,
                    pageToken=next_page_token
                ).execute()
            else:
                break

        return comments

    except HttpError as e:
        print('Erro ao recuperar os comentários:', e)
        return None

#Classifica comentarios do youtube em Negativo (0) e Positivo(1)
def video_youtube(video_id):
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)
    comments = get_video_comments(youtube, video_id)
    data = []
    for item in comments:
        frase = [item]
        resposta = classifica_tweet(frase)
        if resposta[0]==0:
            resposta='Negativo' 
        else: 
            resposta='Positivo'
        data.append({'texto': frase, 'sentimento': resposta})
    return data  

#pega o ID do video do youtube pela url do video
def id_video(link_video):
    parsed_url = urlparse(link_video)
    query_params = parse_qs(parsed_url.query)
    video_id = query_params.get('v', [None])[0]
    return video_id


grafico = {'values': [], 'labels': []}   
server = Flask(__name__)
server.secret_key = 'youtube_comment'
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

#Gerar Grafico
app.layout = html.Div([
    dcc.Store(id='data-store'),
    dcc.Graph(id='pie-chart'),
    dcc.Interval(
        id='interval-component',
        interval=1*1000,
        n_intervals=0
    )
])

app.clientside_callback(
    """
    function(n_intervals) {
        return fetch('/data')
            .then(response => response.json())
            .then(data => data);
    }
    """,
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals')
)

@app.callback(Output('pie-chart', 'figure'),
              Input('data-store', 'data'))
def update_graph(grafico):
    if grafico is None:
        grafico = {'values': [], 'labels': []}
    return {
        'data': [{
            'values': grafico['values'],
            'labels': grafico['labels'],
            'type': 'pie'
        }],
        'layout': {'title': 'Gráfico de Sentimentos dos Comentarios do seu Vídeo'}
    }
    
@server.route('/data')
def data():
    return jsonify(grafico)

#Home Page
@server.route('/')
def index():
    return render_template('index.html', titulo='Home')

@server.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')

#Pagina Resultado
@server.route('/youtube', methods=['POST',])
def youtube():
    try:
        link_video=id_video(request.form['link_video'])
        video_data = video_youtube(link_video)
        df = pd.DataFrame(video_data)
        negativo = df["sentimento"].value_counts().get('Negativo', 0)
        positivo = df["sentimento"].value_counts().get('Positivo', 0)
        #Atualiza variavel global que tem os detalhes do gráfico:
        grafico['values'] = [int(negativo), int(positivo)]
        grafico['labels'] = ['Negativo', 'Positivo']
        return render_template('resultado_pesquisa.html', titulo='Resultado',video_id=link_video)
    except:
        #Mensagem de Erro, caso o usuario insira algo invalido
        return render_template('index.html', titulo='Home',erro='Erro na Leitura do ID')

server.run(debug=True)