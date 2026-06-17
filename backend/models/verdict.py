# This Script defines the Class that is the Schema for the Model's Response
# It is what the Backend returns after the Frontend submits a Verdict
# It can also be incomplete as the model can ask a Clarifying question
# Importing Necessary Libraries
from typing import Optional, Literal
from pydantic import BaseModel
from datetime import datetime

# The Class that conatains the model's response and all related info
class Response(BaseModel):
    id: str
    verdict: Literal['True', 'Misleading', 'False', "Unverified"] | None
    response: str | None
    confidence: float | None
    flagged: bool | None = False
    sources: list[str] | None
    status: Literal['failed', 'completed', 'clarification_needed']
    time: datetime