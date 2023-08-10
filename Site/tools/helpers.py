import unidecode
import nltk
from nltk import tokenize
from string import punctuation
import re
#nltk.download("all")

from __init__ import model,vectorizer


def classifica_texto(text):
    test_vectors = vectorizer.transform(trata(text))
    return model.predict(test_vectors)

def remove_emoticons(text):
    emoticon_pattern = r'[:;=][\-\^]?[\)\(DPp@#$&|]'
    return re.sub(emoticon_pattern, '', text)

def trata(resenha):
    # Tokenizadores
    #token_espaco = tokenize.WhitespaceTokenizer()
    token_pontuacao = tokenize.WordPunctTokenizer()

    # Lista de palavras irrelevantes e pontuação
    palavras_irrelevantes = nltk.corpus.stopwords.words("portuguese")
    pontuacao = list(punctuation)
    pontuacao_stopwords = pontuacao + palavras_irrelevantes

    # Removendo acentos e pontuação
    sem_acentos = [unidecode.unidecode(texto) for texto in resenha]
    stopwords_sem_acento = [unidecode.unidecode(texto) for texto in pontuacao_stopwords]
    resenha = sem_acentos

    # Processando o texto
    frase_processada = []
    for opiniao in resenha:
        nova_frase = []
        opiniao = remove_emoticons(opiniao.lower())
        palavras_texto = token_pontuacao.tokenize(opiniao)
        for palavra in palavras_texto:
            if palavra not in stopwords_sem_acento:
                nova_frase.append(palavra)
        frase_processada.append(' '.join(nova_frase))

    # Reduzindo as palavras ao seu radical
    resenha = frase_processada
    stemmer = nltk.RSLPStemmer()
    frase_processada = []
    for opiniao in resenha:
        nova_frase = []
        opiniao = opiniao.lower()
        palavras_texto = token_pontuacao.tokenize(opiniao)
        for palavra in palavras_texto:
            if palavra not in stopwords_sem_acento:
                nova_frase.append(stemmer.stem(palavra))
        frase_processada.append(' '.join(nova_frase))

    # Retornando o texto processado
    resenha = frase_processada
    return resenha 