from datetime import datetime, timezone
from bson import ObjectId
from pymongo import DESCENDING
from db.mongo import claims
from core.config import SKIP, LIMIT, THRESHOLD


def _serialize(doc: dict) -> dict:
    doc["id"] = str(doc.pop("_id"))
    if isinstance(doc.get("time"), datetime) and doc["time"].tzinfo is None:
        doc["time"] = doc["time"].replace(tzinfo=timezone.utc)
    return doc


async def save_claim(data: dict) -> str:
    doc = {k: v for k, v in data.items() if k != "id"}
    doc.setdefault("time", datetime.now(timezone.utc))
    result = await claims.insert_one(doc)
    return str(result.inserted_id)


async def get_claims(verdict: str = None, limit: int = LIMIT, skip: int = SKIP) -> list:
    query = {}
    if verdict:
        query["verdict"] = verdict
    rows = claims.find(query).sort("time", DESCENDING).limit(limit=limit).skip(skip=skip)
    docs = await rows.to_list(length=limit)
    return [_serialize(doc) for doc in docs]


async def get_by_id(id: str) -> dict | None:
    doc = await claims.find_one({"_id": ObjectId(id)})
    return _serialize(doc) if doc else None


async def delete_by_id(id: str) -> None:
    await claims.delete_one({"_id": ObjectId(id)})


async def update_claim(model_output: dict, id: str) -> None:
    confidence = model_output.get("confidence")
    if isinstance(confidence, (int, float)):
        model_output["flagged"] = confidence < THRESHOLD
    await claims.update_one(
        {"_id": ObjectId(id)},
        {"$set": model_output}
    )