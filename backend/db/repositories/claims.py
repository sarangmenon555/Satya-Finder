from bson import ObjectId
from db.mongo import claims
from datetime import datetime
from pymongo import DESCENDING
from core.config import SKIP, LIMIT, THRESHOLD


async def create_claim(text: str, image_id: str = None) -> str:
    doc = {
        "type": "claim",
        "claim": text,
        "image": image_id,
        "status": "processing",
        "verdict": None,
        "explanation": None,
        "sources": [],
        "confidence": None,
        "flagged": None,
        "time": datetime.now()
    }
    result = await claims.insert_one(doc)
    return str(result.inserted_id)


async def save_claim(data: dict) -> str:
    data.setdefault("time", datetime.now())
    result = await claims.insert_one(data)
    return str(result.inserted_id)


async def update_claim(model_output: dict, id: str):
    model_output.update(
        {"flagged": (model_output.get("confidence") < THRESHOLD)}
    )
    await claims.update_one(
        {"_id": ObjectId(id)},
        {"$set": model_output}
    )


async def get_by_id(id: str) -> dict:
    return await claims.find_one({"_id": ObjectId(id)})


async def delete_by_id(id: str) -> None:
    await claims.delete_one({"_id": ObjectId(id)})


async def get_claims(verdict: str = None, limit: int = LIMIT, skip: int = SKIP) -> list:
    query = {"type": "claim"}
    if verdict:
        query["verdict"] = verdict

    rows = claims.find(query).sort("time", DESCENDING).limit(limit=limit).skip(skip=skip)
    docs = await rows.to_list(length=limit)
    return docs