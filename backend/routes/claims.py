import uuid
import os
import asyncio
import httpx
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException
from models.claim import Claim
from models.verdict import Response
from core.config import THRESHOLD, LIMIT, SKIP
from db.repositories.claims import save_claim, get_claims

router = APIRouter(prefix="/api", tags=["claims"])

AGENT_URL = os.getenv("AGENT_URL")


async def _call_agent(payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=180) as client:
        for attempt in range(5):
            try:
                response = await client.post(f"{AGENT_URL}/verify", json=payload)
                if response.status_code == 502:
                    await asyncio.sleep(20)
                    continue
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 502:
                    await asyncio.sleep(20)
                    continue
                raise
    raise HTTPException(status_code=503, detail="Agent unavailable after retries.")


@router.post("/check", response_model=Response)
async def check_claim(body: Claim) -> Response:
    try:
        payload = {"claim": body.claim}
        if body.image:
            payload["image"] = body.image
        result = await _call_agent(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline error: {e}")

    confidence = result.get("confidence")
    flagged = isinstance(confidence, (int, float)) and confidence * 100 < THRESHOLD

    status = result.get("status", "failed")
    question = result.get("question")
    if status == "failed" and question:
        status = "clarification_needed"

    record = Response(
        id=str(uuid.uuid4()),
        verdict=result.get("verdict"),
        response=result.get("response") or question,
        confidence=confidence,
        flagged=flagged,
        sources=result.get("sources") or [],
        status=status,
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