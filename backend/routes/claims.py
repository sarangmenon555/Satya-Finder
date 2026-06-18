import uuid
import sys
import os
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

AGENT_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "agent")
if AGENT_PATH not in sys.path:
    sys.path.insert(0, os.path.abspath(AGENT_PATH))

from models.claim import Claim
from models.verdict import Response
from core.config import THRESHOLD, LIMIT, SKIP
from db.repositories.claims import save_claim, get_claims

router = APIRouter(prefix="/api", tags=["claims"])


@router.post("/check", response_model=Response)
async def check_claim(body: Claim) -> Response:
    from core.pipeline import run_pipeline

    try:
        result = run_pipeline(body.claim)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    confidence = result.get("confidence")
    flagged = isinstance(confidence, (int, float)) and confidence * 100 < THRESHOLD

    record = Response(
        id=str(uuid.uuid4()),
        verdict=result.get("verdict"),
        response=result.get("response") or result.get("question"),
        confidence=confidence,
        flagged=flagged,
        sources=result.get("sources") or [],
        status=result.get("status", "failed"),
        time=datetime.now(timezone.utc),
    )

    try:
        await save_claim(record.model_dump())
    except Exception:
        pass

    return record


@router.get("/claims", response_model=list[Response])
async def list_claims() -> list[Response]:
    try:
        rows = await get_claims(limit=LIMIT, skip=SKIP)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    return rows
