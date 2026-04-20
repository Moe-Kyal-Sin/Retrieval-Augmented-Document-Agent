from app.utils.text import extract_keywords

class RetrievalAgent():
    '''' Simple Retrieval Agent : Given a list of text, try to find the top k most relavant chunk
    from the list'''
    def run(self, chunks:list[str], question:str, top_k:int = 10):
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