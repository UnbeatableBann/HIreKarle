from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text: str) -> list:
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def calculate_similarity(self, embedding1: list, embedding2: list) -> float:
        emb1 = np.array(embedding1).reshape(1, -1)
        emb2 = np.array(embedding2).reshape(1, -1)
        similarity = cosine_similarity(emb1, emb2)[0][0]
        return float(similarity)

embedding_service = EmbeddingService()