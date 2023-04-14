import pickle

# Carregar o modelo treinado a partir do arquivo
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# Dados de teste
test_data = ['O Twitter está quebrado. Obrigado, Elon. Cerca de seis meses atrás, Elon Musk comprou seu bar favorito da vizinhança. Pelas próprias contas de Musk, o Twitter agora vale menos da metade do que ele pagou. Perdeu  grandes anunciantes e muitos funcionários.']

# Fazer a previsão
prediction = model.predict(test_data)

print(prediction)