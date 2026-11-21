import os
from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAI

app = FastAPI(title="AdmissionFlow AI Service", version="0.1.0")
client = OpenAI() if os.getenv("OPENAI_API_KEY") else None

class FAQRequest(BaseModel):
    question: str = Field(min_length=2, max_length=1000)
    institute_name: str = Field(min_length=1, max_length=150)
    approved_facts: list[str] = Field(min_length=1, max_length=50)
    language: str = "Hinglish"

@app.get("/health")
def health(): return {"status":"ok"}

@app.post("/api/v1/faq/answer")
def answer_faq(payload: FAQRequest, x_service_key: str | None = Header(default=None)):
    key = os.getenv("SERVICE_API_KEY")
    if not key or x_service_key != key:
        raise HTTPException(401, "Invalid service credentials")
    if not client:
        return {"answer":"A counsellor will help you with this question. Please contact the institute.", "escalate_to_human":True}
    facts = "\n".join(f"- {fact}" for fact in payload.approved_facts)
    result = client.chat.completions.create(
        model=os.getenv("OPENAI_MODEL","gpt-4o-mini"), temperature=0.2,
        messages=[
          {"role":"system","content":f"You are an admissions FAQ assistant for {payload.institute_name}. Answer ONLY from these approved facts: {facts}. Never invent fees, dates, placement claims or eligibility. If facts do not answer the question, say so and escalate to a human. Reply in {payload.language}."},
          {"role":"user","content":payload.question}
        ])
    return {"answer":result.choices[0].message.content,"escalate_to_human":False}

