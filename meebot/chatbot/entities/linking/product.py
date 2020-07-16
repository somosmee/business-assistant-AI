'''
 Entity linking
'''
from ..linking.vector_model import VectorModel


class ProductNEL:

    def __init__(self, db, corpus, doc_ids):
        self.db = db
        self.model = VectorModel(corpus, doc_ids)

    def get_similarest(self, query):
        similars = self.model.get_similars(query, limit=5)
        if similars is None:
            return None
        return similars[0]
