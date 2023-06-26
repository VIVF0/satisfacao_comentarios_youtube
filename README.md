# ProjetoIntegradorV_SatisfacaoTweets
### Análise de Sentimentos em Comentários do YouTube
Este é um projeto que utiliza Python para implementar uma IA capaz de realizar análise de sentimentos em comentários do YouTube. O projeto é dividido em duas partes principais: a criação da IA e o desenvolvimento do backend do site.

#### Criação da IA
Na criação da IA, foi utilizada principalmente a linguagem Python, tanto para a implementação da IA quanto para o backend do site. Python foi escolhido devido à sua versatilidade e à sua força na área de Inteligência Artificial.

#### Foram utilizadas as seguintes bibliotecas na criação da IA:

NLTK: Utilizada para a tokenização e limpeza das frases analisadas. O NLTK fornece stopwords, que são palavras consideradas irrelevantes para o processamento da IA (por exemplo: "de", "a", "o", "e", "da", "do", "se", entre outras), que foram removidas das frases durante o treinamento e análise da IA. Além disso, foram realizados outros tratamentos nos textos, como remoção de acentos, pontuações e uso do radical das palavras.

Scikit-learn: Essencial no treinamento da IA, essa biblioteca oferece funções que possibilitam o treinamento de uma IA com base na frequência de palavras para definir pesos para cada uma delas. Utilizando uma relação entre a frequência das palavras e a classificação do modelo de treinamento, a IA consegue criar um algoritmo para classificar novas frases.

Pandas: Utilizada para transformar a fonte de dados, que estava em um arquivo do Excel .csv, em um dataset em pandas. O uso do dataset em pandas facilitou o tratamento das palavras, como a conversão dos sentimentos positivos e negativos para 1 e 0, respectivamente, e permitiu o processamento mais eficiente dos dados.

Pickle: Utilizada para armazenar o treinamento da IA em um arquivo externo e permitir o uso da IA em outros arquivos. Isso possibilitou a utilização da IA no backend do site para classificar os sentimentos dos comentários dos vídeos.

#### Backend do Site
No desenvolvimento do backend do site, foram utilizadas as seguintes bibliotecas principais:

Flask: Biblioteca utilizada para o funcionamento do backend do site. O Flask é considerado um mini framework do Python e foi escolhido devido à sua facilidade e simplicidade em relação a outras frameworks para essa finalidade.

Googleapiclient: Utilizada para se conectar à API V3 do YouTube e obter os comentários dos vídeos.

Dash: Utilizada para a criação de gráficos interativos na página de resultados.

O backend do site foi construído utilizando rotas de URL, onde foram definidas as rotas para retornar gráficos dos comentários do YouTube, exibir a página inicial, a página "Sobre" e a página de resultados com o gráfico da divisão dos comentários de um vídeo do YouTube.

### Como Executar o Projeto
Para executar o projeto, siga as etapas abaixo:

Clone o repositório para sua máquina local:
```
git clone https://github.com/VIVF0/satisfacao_comentarios_youtube
```
Instale as dependências necessárias para a IA e o site:
```
pip install -r IA/requirements.txt
pip install -r Site/requirements.txt
```
Execute o script principal do backend do site:
```
python Site/app.py
```

### Fontes de Dados
IMDB PT-BR dataset: Dataset utilizado para treinamento da IA: https://www.kaggle.com/datasets/luisfredgs/imdb-ptbr 

API V3 do YouTube: Utilizada para obtenção dos comentários dos vídeos: https://developers.google.com/youtube/v3/docs/commentThreads/list?hl=pt-br 

### Referências
Documentação Pandas: https://pandas.pydata.org/docs/getting_started/install.html

Documentação Scikit-learn: https://scikit-learn.org/stable/tutorial/index.html 

Documentação NLTK: https://www.nltk.org/

Documentação Pickle: https://docs.python.org/3/library/pickle.html

Documentação Flask: https://flask.palletsprojects.com/en/2.3.x/

Este projeto está licenciado sob a licença MIT. Sinta-se à vontade para usar, modificar e distribuir este código.
