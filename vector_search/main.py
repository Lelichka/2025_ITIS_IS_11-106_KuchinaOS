import pandas as pd
import math
from collections import Counter

from vector_search.lemmatizer import process_query

# Загрузка необходимых данных из файлов, созданных на предыдущих этапах
def load_data(tfidf_file="../tf-idf/tf_idf_results.xlsx"):

    tfidf_df = pd.read_excel(tfidf_file, sheet_name='TF-IDF', index_col=0)

    # Загрузка TF-IDF (doc_id -> term: tf-idf)
    tfidf_dict = {}
    for doc_id in tfidf_df.columns:
        tfidf_dict[doc_id] = tfidf_df[doc_id].to_dict()

    idf_df = pd.read_excel(tfidf_file, sheet_name='IDF', index_col=0)

    # Загрузка IDF (терм -> значение)
    idf_data = idf_df['IDF'].to_dict()

    return idf_data, tfidf_dict

# Функция для векторизации поискового запроса
def vectorize_query(query, idf_vector):
    query_tokens = process_query(query)
    vector = {}
    token_counts = Counter(query_tokens)
    num_query_tokens = len(query_tokens) if query_tokens else 1e-9 # Avoid division by zero
    for term, count in token_counts.items():
        if term in idf_vector:
            tf = count / num_query_tokens
            vector[term] = tf * idf_vector[term]
        else:
            vector[term] = 0
    return vector

# Функция для расчета косинусного сходства
def cosine_similarity(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# Основная функция поисковой системы
def search(query,idf_vector, tfidf_dict):
    query_vector = vectorize_query(query, idf_vector)
    results = {}
    print(query_vector)
    for doc_id, tfidf_vector in tfidf_dict.items():
        similarity = cosine_similarity(query_vector, tfidf_vector)
        results[doc_id] = similarity
    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    return [(doc_id, score) for doc_id, score in sorted_results]

if __name__ == "__main__":
    data = load_data()
    if data:
        idf_data, tfidf_dict = data
        while True:
            search_query = input("Введите поисковый запрос (или 'выход' для завершения): ")
            if search_query.lower() == 'выход':
                break

            search_results = search(search_query, idf_data, tfidf_dict)
            if search_results:
                print("\nРезультаты поиска:")
                for doc_id, score in search_results:
                    print(f"Документ №{doc_id}: Релевантность = {score:.6f}")
            else:
                print("Нет результатов, соответствующих запросу.")

    else:
        print("Не удалось загрузить необходимые данные. Пожалуйста, проверьте файлы.")