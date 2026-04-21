from app.services.retrieval import RetrievalAgent
from app.services.answer import AnswerAgent

class Orchestrator():
    ''' Retrieve related chunks using retrieval agent and answer the question using answer agent'''
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.answer_agent = AnswerAgent()
    def run(self, question:str, document_id:str):
        top_k = 6
        top_k_chunks = self.retrieval_agent.run(document_id, question, top_k=top_k)
        response = self.answer_agent.run(question, top_k_chunks)
        top_k_chunks_and_score = [f"score : {dict_chunk['score']},\nchunk : {dict_chunk['chunk']}" for dict_chunk in top_k_chunks]
        return {'response': response,
                'top_chunks': top_k_chunks_and_score}
        