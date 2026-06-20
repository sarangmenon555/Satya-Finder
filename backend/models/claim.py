from pydantic import BaseModel, Field
from typing import Optional, Literal


class Claim(BaseModel):
    claim: str = Field(..., min_length=1, max_length=2000)
    image: Optional[str] = Field(default=None, max_length=8000000)