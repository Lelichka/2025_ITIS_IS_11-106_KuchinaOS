import os
import json
from collections import defaultdict

from boolean_search import BooleanSearch

INPUT_DIR = '../cleared_documents'
inverted_index_file = '../inverted_index.json'

def load_documents_from_folder(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                tokens = file.read().strip().split()
                documents[filename] = tokens
    return documents

def create_inverted_index(docs):
    index = defaultdict(list)
    for doc_id, tokens in docs.items():
        unique_tokens = set(tokens)
        for token in unique_tokens:
            index[token].append(doc_id)
    return dict(sorted(index.items()))

def create_index_file():
    documents = load_documents_from_folder(INPUT_DIR)
    inverted_index = create_inverted_index(documents)

    with open(inverted_index_file, 'w', encoding='utf-8') as f:
        json.dump(inverted_index, f,ensure_ascii=False)

def main():

    #create_index_file()

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
    ]

    for query in queries:
        result = search_engine.search(query)
        print(f"Query: '{query}', Result: {len(result)} : {result}")

if __name__ == '__main__':
    main()


