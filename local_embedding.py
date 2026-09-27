import torch
from vector_index import VectorIndex
from transformers import AutoTokenizer, AutoModel

class LocalEmbedding:

  def __init__(self,model_name="sentence-transformers/all-MiniLM-L6-v2", distance_metric="cosine"):
    self.model_name = model_name
    self.device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"[LocalEmbedding] Loading {self.model_name} on {self.device}...")
    self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
    self.model = AutoModel.from_pretrained(self.model_name)
    self.model.to(self.device)
    self.model.eval()
    print("[LocalEmbedding] Model ready.")

    self.store = VectorIndex(distance_metric=distance_metric, embedding_fn=self._embed_one,)

