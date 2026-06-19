from fastapi import FastAPI
from pydantic import BaseModel
from core.pipeline import run_pipeline

app = FastAPI()


class ClaimRequest(BaseModel):
    claim: str


@app.post("/verify")
def verify(request: ClaimRequest):
    return run_pipeline(request.claim)