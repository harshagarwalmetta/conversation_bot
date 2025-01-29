from fastapi import FastAPI
from pydantic import BaseModel
from app.rag import get_rag_response

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(query: Query):
    response = get_rag_response(query.question)
    return {"response": response}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}