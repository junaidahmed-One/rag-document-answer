import numpy as np

class VectorIndex:
    def __init__(self, distance_metric="cosine", embedding_fn=None):
        self.distance_metric = distance_metric
        self.embedding_fn = embedding_fn
        self.vectors = []
        self.metadata = []

    def add(self, text, vector):
        self.vectors.append(vector)
        self.metadata.append(text)

    def _cosine_similarity(self, v1, v2):
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0
        return dot_product / (norm_v1 * norm_v2)

    def search(self, query_vector, k=5):
        if not self.vectors:
            return []
        similarities = [self._cosine_similarity(query_vector, v) for v in self.vectors]
        top_indices = np.argsort(similarities)[::-1][:k]
        return [(self.metadata[i], similarities[i]) for i in top_indices]
