from tools import *
from src import *
from app import *
from views import *
import pickle
#Carrega Modelo:
model = pickle.load(open('AI/lrModel', "rb"))
vectorizer = pickle.load(open("AI/vectorizer", "rb"))