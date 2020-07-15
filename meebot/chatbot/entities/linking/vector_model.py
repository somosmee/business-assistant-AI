import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


class VectorModel:
    def __init__(self, corpus, doc_ids):
        self.corpus = corpus
        self.doc_ids = doc_ids
        self.vectorizer = TfidfVectorizer(
            encoding='latin1', strip_accents='unicode', lowercase=True)
        self.docs_tfidf = self.vectorizer.fit_transform(corpus)

    def get_similars(self, query, limit=5):
        query_vector = self.vectorizer.transform([query])
        similarity_matrix = cosine_similarity(self.docs_tfidf, query_vector)
        results = self.get_products_from_similarities(similarity_matrix, self.doc_ids, limit=limit)
        return results

    def get_products_from_similarities(self, similarity_matrix, doc_ids, limit=5):
        products = []
        sorted_indexes = np.argsort(similarity_matrix, axis=0)

        for index in sorted_indexes[:-limit:-1]:
            products.append(
                {'id': doc_ids[index[0]],
                 'doc': self.corpus[index[0]],
                 'distance': similarity_matrix[index[0]][0]})

        return products
