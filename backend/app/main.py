from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from jose import jwt, JWTError
from datetime import datetime, timezone
from uuid import uuid4
import os, psycopg

app = FastAPI(title="AdmissionFlow API", version="0.1.0")
DB = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/admissionflow")
SECRET = os.getenv("JWT_SECRET", "dev-only-change-me")

def db():
    return psycopg.connect(DB, row_factory=psycopg.rows.dict_row)

def claims(authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Bearer token required")
    try:
        data = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
        if not data.get("sub") or not data.get("org"): raise ValueError()
        return data
    except (JWTError, ValueError):
        raise HTTPException(401, "Invalid token")

class LeadIn(BaseModel):
    organization_id: str
    student_name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=8, max_length=20)
    email: str | None = None
    source: str = "other"
    status: str = "new"
    notes: str | None = None
    consent_to_contact: bool = False

@app.get("/health")
def health(): return {"status":"ok"}

@app.get("/api/v1/leads")
def list_leads(organization_id: str, auth=Depends(claims)):
    if auth["org"] != organization_id: raise HTTPException(403, "Forbidden")
    with db() as conn:
        rows = conn.execute("SELECT * FROM leads WHERE organization_id=%s ORDER BY created_at DESC LIMIT 100",(organization_id,)).fetchall()
    return {"data":rows}

@app.post("/api/v1/leads", status_code=201)
def create_lead(item: LeadIn, auth=Depends(claims)):
    if auth["org"] != item.organization_id: raise HTTPException(403, "Forbidden")
    if item.status not in {"new","contacted","interested","enrolled","lost"}: raise HTTPException(422,"Invalid status")
    with db() as conn:
        row = conn.execute("""INSERT INTO leads
        (id,organization_id,student_name,phone,email,source,status,notes,consent_to_contact)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING *""",
        (str(uuid4()),item.organization_id,item.student_name,item.phone,item.email,item.source,item.status,item.notes,item.consent_to_contact)).fetchone()
    return {"data":row}
