import googleapiclient
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from urllib.parse import urlparse, parse_qs
import pandas as pd 

import os
from dotenv import load_dotenv
load_dotenv()
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
DEVELOPER_KEY =  os.getenv('DEVELOPER_KEY')
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey = DEVELOPER_KEY)

from tools import *
class Video:
    def __init__(self, link_video):
        self.link_video = link_video
        self.id_video = self.id
        self.comentarios_youtube = self.get_video_comments()
        self.dataset = self.video_youtube()

    @property
    def id(self):
        parsed_url = urlparse(self.link_video)
        query_params = parse_qs(parsed_url.query)
        id_video = query_params.get('v', [None])[0]
        return id_video

    def sentimento_positivo(self):
        return self.dataset["sentimento"].value_counts().get('Positivo', 0)

    def sentimento_negativo(self):
        return self.dataset["sentimento"].value_counts().get('Negativo', 0)

    def video_youtube(self):
        data = []
        for item in self.comentarios_youtube:
            frase = [item]
            resposta = classifica_tweet(frase)
            if resposta[0] == 0:
                resposta = 'Negativo'
            else:
                resposta = 'Positivo'
            data.append({'texto': frase, 'sentimento': resposta})
        return pd.DataFrame(data)

    def get_video_comments(self):
        try:
            comments = []
            # Primeira solicitação para obter os comentários principais
            results = youtube.commentThreads().list(
                part='snippet',
                videoId=self.id_video,
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
                        videoId=self.id_video,
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