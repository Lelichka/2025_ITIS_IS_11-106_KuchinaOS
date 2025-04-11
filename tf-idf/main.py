import json
import math
import pandas as pd

updated_inverted_index_file = '../updated_inverted_index.json'
with open(updated_inverted_index_file, 'r', encoding='utf-8') as f:
    inverted_index = json.load(f)

num_documents = 100

# 1. Calculate TF
tf_data = {}
all_documents = set()
for term, doc_counts in inverted_index.items():
    tf_data[term] = {}
    for doc_id, count in doc_counts:
        tf_data[term][doc_id] = count
        all_documents.add(doc_id)

tf_df_data = {}
for term, doc_freqs in tf_data.items():
    tf_df_data[term] = doc_freqs
tf_df = pd.DataFrame.from_dict(tf_df_data, orient='index').fillna(0)

# Calculate IDF
idf_data = {}
for term, doc_counts in inverted_index.items():
    df = len(doc_counts)
    idf = math.log10(num_documents / df) if df > 0 else 0.0
    idf_data[term] = round(idf, 6)

idf_df = pd.DataFrame.from_dict(idf_data, orient='index', columns=['IDF'])

# Calculate TF-IDF
tfidf_data = {}
for term, tf_values in tf_data.items():
    tfidf_data[term] = {}
    idf = idf_data.get(term, 0.0)
    for doc_id, tf in tf_values.items():
        tfidf_data[term][doc_id] = round(tf * idf, 6)

tfidf_df = pd.DataFrame.from_dict(tfidf_data, orient='index').fillna(0)

# Save to Excel file
excel_file = 'tf_idf_results.xlsx'
with pd.ExcelWriter(excel_file) as writer:
    tf_df.to_excel(writer, sheet_name='TF', float_format='%.6f')
    idf_df.to_excel(writer, sheet_name='IDF', float_format='%.6f')
    tfidf_df.to_excel(writer, sheet_name='TF-IDF', float_format='%.6f')

print(f"TF, IDF, and TF-IDF tables have been saved to '{excel_file}'.")