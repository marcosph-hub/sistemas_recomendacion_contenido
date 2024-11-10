import math
import json
import argparse
import numpy as np
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def laod_documents(filename):
    with open(filename, 'r') as f:
        return [line.strip() for line in f.readlines()]
    
def load_stopwords(filename):
    with open(filename, 'r') as f:
        stopwords = set(f.read().splitlines())
    return stopwords

def load_lematization(file_path):
    with open(file_path, 'r') as f:
        lematization = json.load(f)
    return lematization

def process_document(document, stopwords, lemmatization_dict):
    tokens = document.lower().split()
    processed_tokens = [lemmatization_dict.get(token, token) for token in tokens if token not in stopwords]
    return processed_tokens

def calculate_tf(document_tokens):
    tf = {}
    for term in document_tokens:
        tf[term] = tf.get(term, 0) + 1
    total_terms = len(document_tokens)
    return {term: freq / total_terms for term, freq in tf.items()}

def calculate_idf(documents):
    idf = {}
    total_documents = len(documents)
    for document in documents:
        for term in set(document):
            idf[term] = idf.get(term, 0) + 1
    return {term: math.log(total_documents / freq) for term, freq in idf.items()}

def calculate_tfidf(tf, idf):
    return {term: tf_value * idf.get(term, 0) for term, tf_value in tf.items()}

def create_tfidf_matrix(tokens_matrix,idf_dict):
    vocabulary = list(set(term for doc in tokens_matrix for term in doc))
    tfidf_matrix = []

    for token in tokens_matrix:
        tf = calculate_tf(token)
        tfidf = calculate_tfidf(tf, idf_dict)
        tfidf_vector = [tfidf.get(term, 0) for term in vocabulary]
        tfidf_matrix.append(tfidf_vector)

    return tfidf_matrix

def cosine_similarity(vec_a, vec_b):
    dot_product = np.dot(vec_a, vec_b)

    norm_a = np.linalg.norm(vec_a)
    norm_b = np.linalg.norm(vec_b)
    
    return dot_product / (norm_a * norm_b)

def calculate_cosine_similarities(tfidf_matrix):
    num_documents = len(tfidf_matrix)
    cosine_similarities = np.zeros((num_documents, num_documents))  
    
    for i in range(num_documents):
        for j in range(i, num_documents):
            similarity = cosine_similarity(tfidf_matrix[i], tfidf_matrix[j])
            cosine_similarities[i][j] = similarity
            cosine_similarities[j][i] = similarity
    
    return cosine_similarities

def create_table(terms, tf, idf, tfidf):
    df = pd.DataFrame({
        'Index': range(1, len(terms) + 1),
        'Term': terms,
        'TF': [tf.get(term, 0) for term in terms],
        'IDF': [idf.get(term, 0) for term in terms],
        'TF-IDF': [tfidf.get(term, 0) for term in terms]
    })
    return df

def main():
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en el contenido")
    parser.add_argument('document_file', help="Archivo con los documentos")
    parser.add_argument('stopwords_file', help="Archivo con las palabras de parada")
    parser.add_argument('lemmatization_file', help="Archivo de lematización de términos")
    args = parser.parse_args()
    
    document_container = laod_documents(args.document_file)
    stopwords = load_stopwords(args.stopwords_file)
    lematization = load_lematization(args.lemmatization_file)

    all_tokens_matrix = [process_document(doc, stopwords, lematization) for doc in document_container]
    
    tf_list = [calculate_tf(doc_token) for doc_token in all_tokens_matrix]
    idf_dict = calculate_idf(all_tokens_matrix)
    tf_idf_dict = [calculate_tfidf(tf_doc, idf_dict) for tf_doc in tf_list]

    for i, (doc, tfidf) in enumerate(zip(all_tokens_matrix, tf_idf_dict), start=1):
        terms = list(tfidf.keys())
        tf = calculate_tf(doc)
        tfidf_vals = calculate_tfidf(tf, idf_dict)
        df = create_table(terms, tf, idf_dict, tfidf_vals)
        print(f"Documento {i}")
        print(df)

    tfidf_matrix = create_tfidf_matrix(all_tokens_matrix, idf_dict)
    cosine_similarities = calculate_cosine_similarities(tfidf_matrix)
    print("Matriz de Similitud Coseno:")

    cosine_similarities_df = pd.DataFrame(cosine_similarities, index=[f'Document {i+1}' for i in range(len(tfidf_matrix))], columns=[f'Document {i+1}' for i in range(len(tfidf_matrix))])
    
    print(cosine_similarities_df)

if __name__ == "__main__":
    main()