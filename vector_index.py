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

    def add_vector(self, vector, metadata):
        self.vectors.append(vector)
        self.metadata.append(metadata)

    def _cosine_similarity(self, v1, v2):
        v1 = np.array(v1, dtype=float)
        v2 = np.array(v2, dtype=float)
        dot_product = np.dot(v1, v2)
        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)
        if norm_v1 == 0 or norm_v2 == 0:
            return 0
        return dot_product / (norm_v1 * norm_v2)

    def search(self, query_vector, k=5):
        if not self.vectors:
            return []
        
        # If a string query is passed and we have an embedding function, embed it first
        if isinstance(query_vector, str):
            if self.embedding_fn is not None:
                query_vector = self.embedding_fn(query_vector)
            else:
                raise ValueError("A string query was provided, but no embedding_fn is configured on this VectorIndex.")

        similarities = [self._cosine_similarity(query_vector, v) for v in self.vectors]
        top_indices = np.argsort(similarities)[::-1][:k]
        return [(self.metadata[i], similarities[i]) for i in top_indices]
