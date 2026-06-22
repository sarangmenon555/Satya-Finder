from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from core.pipeline import run_pipeline

app = FastAPI()

class ClaimRequest(BaseModel):
    claim: str
    image: Optional[str] = None

@app.get("/health")
def health():
    return {"status": "running"}

@app.post("/verify")
def verify(request: ClaimRequest):
    return run_pipeline(request.claim, request.image)