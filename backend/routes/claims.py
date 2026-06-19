import uuid
import os
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException

from models.claim import Claim
from models.verdict import Response
from core.config import THRESHOLD, LIMIT, SKIP
from db.repositories.claims import save_claim, get_claims

router = APIRouter(prefix="/api", tags=["claims"])

AGENT_URL = os.getenv("AGENT_URL")


@router.post("/check", response_model=Response)
async def check_claim(body: Claim) -> Response:
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            agent_response = await client.post(f"{AGENT_URL}/verify", json={"claim": body.claim})
            agent_response.raise_for_status()
            result = agent_response.json()
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