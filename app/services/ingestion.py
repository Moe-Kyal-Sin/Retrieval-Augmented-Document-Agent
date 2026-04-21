from pathlib import Path
from pypdf import PdfReader
from fastapi import HTTPException
from app.utils.text import clean_text, chunk_text
from app.services.embedding import EmbeddingService
from app.services.vectorStore import VectorStore
class IngestionAgent:
    ''' Extract text from plain/text file and application/pdf file and preprocess them'''
    def extract_text(self, file_path: Path, content_type: str):
        if content_type == 'text/plain':
            try :
                raw_text = file_path.read_text(encoding = 'utf-8')
            except UnicodeDecodeError:
                raw_text = file_path.read_text(encoding='latin-1')
            return raw_text
        elif content_type == 'application/pdf':
            try:
                reader = PdfReader(file_path)
                pages_text = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text.strip():
                        pages_text.append(page_text)
                raw_text = "\n\n".join(pages_text)
                return raw_text
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Cannot read pdf {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="Unsupport Type Found. ONlY TXT AND PDF")

    def run(self, file_path: Path, content_type: str):
        embedding_model = EmbeddingService()
        vector_store = VectorStore()
        
        raw_text = self.extract_text(file_path, content_type)
        cleaned_text = clean_text(raw_text)
        chunks = chunk_text(cleaned_text, chunk_size = 500, overlap = 100)
        
        embedding = embedding_model.embed_chunks(chunks)
        faiss_index = vector_store.vector_store(embedding)

        return {'text': cleaned_text,
                'chunks': chunks,
                'embedding': embedding,
                'faiss_index': faiss_index}    