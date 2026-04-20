from app.services.retrieval import RetrievalAgent
from app.services.answer import AnswerAgent

class Orchestrator():
    ''' Retrieve related chunks using retrieval agent and answer the question using answer agent'''
    def __init__(self):
        self.retrieval_agent = RetrievalAgent()
        self.answer_agent = AnswerAgent()
    def run(self, question:str, chunks:list[str]):
        top_k = 6
        top_k_chunks = self.retrieval_agent.run(chunks, question, top_k=top_k)
        response = self.answer_agent.run(question, top_k_chunks)
        return response
        