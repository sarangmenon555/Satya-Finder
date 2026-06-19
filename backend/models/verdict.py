from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime


class Response(BaseModel):
    id: str
    verdict: Literal['True', 'Misleading', 'False', 'Unverified'] | None
    response: str | None
    confidence: float | None
    flagged: bool | None = False
    sources: list[str] | None
    status: Literal['failed', 'completed', 'processing', 'clarification_needed']
    time: datetime