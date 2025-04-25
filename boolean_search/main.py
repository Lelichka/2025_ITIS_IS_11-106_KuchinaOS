import os
import json
import re
from collections import defaultdict

from nltk.corpus.reader import documents

from boolean_search import BooleanSearch

INPUT_DIR = '../cleared_documents'
inverted_index_file = '../inverted_index.json'
updated_inverted_index_file = '../updated_inverted_index.json'
document_tokens_file = "../document_tokens.json"
def load_documents_from_folder(folder_path):
    document_tokens = {}
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                tokens = file.read().strip().split()
                documents[filename] = tokens
                document_tokens[filename] = len(tokens)

    with open(document_tokens_file, 'w', encoding='utf-8') as f:
        json.dump(document_tokens, f,ensure_ascii=False)

    return documents

def create_inverted_index(docs):
    index = defaultdict(list)
    updated_index = defaultdict(list)

    for doc_id, tokens in docs.items():
        unique_tokens = set(tokens)
        for token in unique_tokens:
            index[token].append(doc_id)
            updated_index[token].append((doc_id, tokens.count(token)))
    return dict(sorted(index.items())), dict(sorted(updated_index.items()))

def create_index_file():
    documents = load_documents_from_folder(INPUT_DIR)
    inverted_index, updated_inverted_index = create_inverted_index(documents)

    with open(inverted_index_file, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f,ensure_ascii=False)

    with open(updated_inverted_index_file, 'w', encoding='utf-8') as f:
        json.dump(updated_inverted_index, f,ensure_ascii=False)

def main():

    create_index_file()

    with open(inverted_index_file, 'r', encoding='utf-8') as f:
        inverted_index = json.load(f)

    search_engine = BooleanSearch(inverted_index)

    # queries = [
    #     "наука & растение | учёный",
    #     "наука & !растение | !учёный",
    #     "наука | растение | учёный",
    #     "наука | !растение | !учёный",
    #     "наука & растение & учёный"
    # ]

    queries = [
        "!наука & растение & !учёный",
        "наука & !растение & учёный",
        "наука & растение & учёный",
        "наука & растение | учёный",
    ]

    for query in queries:
        result = search_engine.search(query)
        result = list(result)
        result = list(map(deleteTxt,result))
        result.sort()
        print(f"Query: '{query}', Result: {len(result)} : {result}")

def deleteTxt(doc_name):
    match = re.search(r'\d+', doc_name)

    if match:
        number = match.group(0)
    return int(number)

if __name__ == '__main__':
    main()




