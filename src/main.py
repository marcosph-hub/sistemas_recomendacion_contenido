import pandas as pd
import argparse
import json
import spacy
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

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
    processed_tokens = []
    for token in doc:
        if token.text not in stopwords and token.text.isalpha():
            lemma = lematization.get(token.text, token.lemma_)
            processed_tokens.append(lemma)
    return processed_tokens

def main():
    parser = argparse.ArgumentParser(description="Sistema de recomendación basado en el contenido")
    parser.add_argument('document_file', help="Archivo con los documentos")
    parser.add_argument('stopwords_file', help="Archivo con las palabras de parada")
    parser.add_argument('lemmatization_file', help="Archivo de lematización de términos")
    args = parser.parse_args()
    
    document = laod_documents(args.document_file)
    stopwords = load_stopwords(args.stopwords_file)
    lematization = load_lematization(args.lemmatization_file)
    
    tokens = process_text(document, stopwords, lematization)

    print (tokens)


if __name__ == "__main__":
    main()