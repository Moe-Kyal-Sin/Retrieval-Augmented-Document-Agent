from fastapi import HTTPException
from app.core.config import client

class AnswerAgent():
    '''From top_k most related text, ask llm the quesion and generate a response'''
    def run(self, question:str, retrieved_results:list[dict]):

        if not retrieved_results:
            return "I can't find any related document"
        if not question.strip():
            raise HTTPException(status_code=400, detail='question cannot be empty')
        if client is None:
            raise HTTPException(status_code=500, detail="OpenAi Api might be missing")
        context_text = [f"chunk_index: {result['chunk_index']}, chunk_text: {result['chunk']}" for result in retrieved_results if result['chunk'].strip()]
        context_text = "\n\n".join(context_text)

        prompt = f"""
        You are a helpful document question answering assistant.
        Answer the user question using the context provided below.
        If the answeris not in the context, say i couldn't find the context in provided document

        Context:
        {context_text}
        Question:
        {question}
        """.strip()

        try:
            response = client.responses.create(
                model = 'gpt-5',
                input = prompt
            )
            response_text = response.output_text.strip()
            return response_text
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"LLM Response Failed {str(e)}")