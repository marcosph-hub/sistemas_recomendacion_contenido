import math
import json
import spacy
import argparse
import numpy as np
import pandas as pd
from collections import Counter
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

nlp = spacy.load('en_core_web_sm')


def laod_documents(filename):
    with open(filename, 'r') as f:
        documents = f.readlines()
        return documents
    
def load_stopwords(filename):
    with open(filename, 'r') as f:
        stopwords = set(f.read().splitlines())
    return stopwords

def load_lematization(file_path):
    with open(file_path, 'r') as f:
        lematization = json.load(f)
    return lematization


def process_text(plain_text, stopwords, lematization):
    plain_text = ' '.join(plain_text)
    doc = nlp(plain_text.lower())
    all_terms = []
    for token in doc:
        if token.text not in stopwords and token.text.isalpha():
            lemma = lematization.get(token.text, token.lemma_)
            all_terms.append(lemma)
    return all_terms


def calculate_tf(tokens):
    term_count = Counter(tokens)
    tf = {term: count / len(tokens) for term, count in term_count.items()}
    # tf = {term: round(count / len(tokens), 6) for term, count in term_count.items()}
    return tf

def calculate_idf(documents, all_terms):
    idf = {}
    total_documents = len(documents)
    for term in all_terms:
        doc_freq = sum(1 for doc in documents if term in doc)
        idf[term] = math.log(total_documents / (1 + doc_freq))  # Se usa 1 + doc_freq para evitar división por 0
    return idf

def calculate_tf_idf(tf, idf):
    tf_idf = {}
    for term, tf_value in tf.items():
        if term in idf:
            idf_value = idf[term]
            tf_idf[term] = tf_value * idf_value
        else:
            tf_idf[term] = 0
    return tf_idf

def vectorize_tfidf(tf_idf):
    # vectorizer = TfidfVectorizer()
    # tfidf_matrix = vectorizer.fit_transform(document)


    # terms = list(set(term for doc in tf_idf for term in doc))  # Todos los términos únicos
    # matrix = np.zeros((len(tf_idf), len(terms)))
    # for i, doc in enumerate(tf_idf):
    #     for j, term in enumerate(terms):
    #         matrix[i][j] = doc.get(term, 0)
    return tf_idf

def calculate_cosine_similarity(tfidf_matrix):
    return tfidf_matrix
    # return cosine_similarity(tfidf_matrix)


# def create_table(terms, tf, idf, tfidf,cosine_sim):
#     df = pd.DataFrame({
#         'Index': range(1, len(terms) + 1),
#         'Term': terms,
#         'TF': [tf.get(term, 0) for term in terms],
#         'IDF': [idf.get(term, 0) for term in terms],
#         'TF-IDF': [tfidf.get(term, 0) for term in terms],
#         'Cosine Similarity': [cosine_sim[0][i] for i in range(len(cosine_sim[0]))]
#     })
#     return df

def main():
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en el contenido")
    parser.add_argument('document_file', help="Archivo con los documentos")
    parser.add_argument('stopwords_file', help="Archivo con las palabras de parada")
    parser.add_argument('lemmatization_file', help="Archivo de lematización de términos")
    args = parser.parse_args()
    
    document = laod_documents(args.document_file)
    print (document)
    stopwords = load_stopwords(args.stopwords_file)
    lematization = load_lematization(args.lemmatization_file)
    
    all_terms = process_text(document, stopwords, lematization)

    tf = calculate_tf(all_terms)
    idf = calculate_idf(document, all_terms)
    tf_idf = calculate_tf_idf(tf, idf)
    # print(tf_idf)
    tfidf_matrix = vectorize_tfidf(tf_idf)
    # print (len(tfidf_matrix))
    # print (tfidf_matrix)
    cosine_similarity = calculate_cosine_similarity(tfidf_matrix)

    # df = create_table(all_terms, tf, idf, tf_idf, cosine_similarity)

    # print (df)
    # print(len(all_terms))
    # print(len(document))
    # print(len(tf))
    # print(len(idf))
    # print(len(tf_idf))
    # print(len(cosine_similarity))
    

if __name__ == "__main__":
    main()