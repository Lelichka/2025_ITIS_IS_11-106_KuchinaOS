import os
import nltk
import re
from nltk.corpus import stopwords
import pymorphy3

nltk.download('punkt')
nltk.download('stopwords')



def remove_punctuation(tokens):
    return [token for token in tokens if re.match(r'^[а-яА-ЯёЁ]+$', token)]

def tokenize(text):
    tokens = nltk.word_tokenize(text, language='russian')
    return remove_punctuation(tokens)

def lemmatize(tokens):
    morph = pymorphy3.MorphAnalyzer()
    return [morph.parse(token)[0].normal_form for token in tokens]

def remove_stopwords(tokens):
    stop_words = set(stopwords.words('russian'))
    return [token for token in tokens if token not in stop_words]

def process_query(tokens):
    tokens = tokenize(tokens)
    lemmatized_tokens = lemmatize(tokens)
    filtered_tokens = remove_stopwords(lemmatized_tokens)
    return filtered_tokens
