from app.core.config import client
import openai
from fastapi import HTTPException
class EmbeddingService():
    def __init__(self, client=client, model = 'text-embedding-3-small'):
       self.client = client
       self.model= model
    def embed_chunks(self, chunks:list[str]):
        try:
            response = self.client.embeddings.create(
                model = self.model,
                input = chunks
            )
            embedding = [label.embedding for label in response.data]
            return embedding
        except openai.RateLimitError as e:
            raise HTTPException(status_code=429, detail=f"Embedding failed: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")
    def embed_question(self, question:str):
        try:
            response = self.client.embeddings.create(
                model = self.model,
                input = question
            )
            embedding = response.data[0].embedding
            return embedding
        except openai.RateLimitError as e:
            raise HTTPException(status_code=429, detail=f"Embedding failed: {str(e)}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Embedding failed: {str(e)}")