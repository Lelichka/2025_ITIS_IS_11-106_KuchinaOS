import os
import nltk
import re
from nltk.corpus import stopwords
import pymorphy3

nltk.download('punkt')
nltk.download('stopwords')

INPUT_DIR = '../downloaded_pages'
OUTPUT_DIR = '../cleared_documents'

def load_documents(directory):
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

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

def process_documents(documents, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    processed_docs = []
    i = 0
    for doc in documents:
        tokens = tokenize(doc)
        lemmatized_tokens = lemmatize(tokens)
        filtered_tokens = remove_stopwords(lemmatized_tokens)
        processed_docs.append(filtered_tokens)

        file_name = f'{i}.txt'
        i+=1

        with open(os.path.join(output_directory, file_name), 'w', encoding='utf-8') as file:
            file.write(' '.join(filtered_tokens))

        print(f'Обработан файл {file_name}')

    return processed_docs

if __name__ == "__main__":

    documents = load_documents(INPUT_DIR)
    processed_docs = process_documents(documents, OUTPUT_DIR)

    print(f"Обработано {len(processed_docs)} документов и сохранено в '{OUTPUT_DIR}'.")
