from flask import Flask, render_template, request, redirect, session, flash, url_for,jsonify
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app,server
from src import Video

grafico = {'values': [], 'labels': []}  

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

@server.route('/')
def index():
    return render_template('index.html', titulo='Home')

@server.route('/sobre')
def sobre():
    return render_template('sobre.html', titulo='Sobre')

@server.route('/youtube', methods=['POST',])
def youtube():
    try:
        video = Video(request.form['link_video'])
        negativo = video.sentimento_negativo()
        positivo = video.sentimento_positivo()
        grafico['values'] = [int(negativo), int(positivo)]
        grafico['labels'] = ['Negativo', 'Positivo']
        return render_template('resultado_pesquisa.html', titulo='Resultado', video_id=video.id)
    except:
        #Mensagem de Erro, caso o usuario insira algo invalido
        return render_template('index.html', titulo='Home',erro='Erro na Leitura do ID')