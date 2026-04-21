import faiss
import numpy as np
from fastapi import HTTPException
class VectorStore():
    def __init__(self):
        return
    def vector_store(self, embeddings: list[list[float]]):
        if not embeddings:
            raise HTTPException(status_code=400, detail = "Embeddings are Empty")
        array = np.array(embeddings, dtype='float32') # row x col
        dims = array.shape[1] # row is number of chunks and col is embedded numbers

        faiss.normalize_L2(array) # normalize the array to lenth of 1
        faiss_index = faiss.IndexFlatIP(dims) # dot porduct of normalized array is same as cosine similarity
        faiss_index.add(array)

        return faiss_index        