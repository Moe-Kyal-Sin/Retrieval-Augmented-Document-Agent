from app.utils.text import extract_keywords
from app.core.store import DOCUMENT_STORE
from fastapi import HTTPException
from app.services.embedding import EmbeddingService
import numpy as np

class RetrievalAgent():
    '''' Simple Retrieval Agent : Given a list of text, try to find the top k most relavant chunk
    from the list'''


    def keyword_run(self, question:str, chunks:list[str], top_k:int):
        keywords = extract_keywords(question)
        if not keywords:
            return []
        retrieved_chunks = []
        for i, chunk in enumerate(chunks):
            score = 0
            matched_keywords = []
            for keyword in keywords:
                if keyword in chunk:
                    score += 1
                    matched_keywords.append(keyword)
            retrieved_chunks.append({
                'score': score,
                'chunk_index': i,
                'chunk': chunk,
                'matched_keywords': matched_keywords
            })
        retrieved_chunks.sort(key = lambda x: x['score'], reverse = True)
        return retrieved_chunks[:top_k]
    
    
    def embedding_run(sef, question: str, faiss_index:list[list[float]], chunks:list[str], top_k:int):
        embedding_model = EmbeddingService()
        question_embedding = embedding_model.embed_question(question)
        question_embedding = np.array([question_embedding], dtype="float32")

        distances, indices = faiss_index.search(question_embedding, top_k)
        retrieved_chunks = []
        for score, idx in zip(distances[0], indices[0]): # faiss_search is for multiple queries so it returned list of list
            if idx == -1:
                continue
            else:
                retrieved_chunks.append({
                    'score' : score,
                    'chunk_index': idx,
                    'chunk' : chunks[idx]
                })
        return retrieved_chunks

    def run(self, document_id:str, question:str, top_k:int = 10, mode = "embedding"):
        
        document = DOCUMENT_STORE[document_id]
        chunks = document['chunks']
        if mode == "keyword":
            return self.keyword_run(question, chunks, top_k)
        elif mode == "embedding":
            faiss_index = document['faiss_index']
            return self.embedding_run(question, faiss_index, chunks, top_k)
        else:
            raise HTTPException(status_code = 400, detail = "Invalid Retrieval Mode")