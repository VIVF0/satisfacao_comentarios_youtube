import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs
import pickle

from app import app,server
from tratamento import trata

import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY =  os.getenv('DEVELOPER_KEY')
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