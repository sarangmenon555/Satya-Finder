# This is The Script that defines Classes that make up the API Structure
# It includes the things that the Frontend can call to the Backend
# It mainly includes the Claim, and The Clarification
# Imporitng Necessary Libraries
from pydantic import BaseModel
from typing import Optional, Literal

# The Claim that the user gives
class Claim(BaseModel):
    claim: str
    image: Optional[str] = None
    
# The Answer to the clarification questions the model asked
class Clarification(BaseModel):
    answer: str