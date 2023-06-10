from flask import Flask
import dash
 
server = Flask(__name__)
server.secret_key = 'youtube_comment'
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/')

from views import *

if __name__ == '__main__':
    server.run(debug=True)