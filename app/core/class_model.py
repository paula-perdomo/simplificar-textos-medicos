from pydantic import BaseModel

# --- 2. Define Request/Response Models ---

class GenerateRequest(BaseModel):
    """The input request model containing the abstract text."""
    text: str

class ReadabilityScores(BaseModel):
    """Model for the nested readability scores."""
    CLI: float
    FRE: float
    GFI: float
    SMOG: float
    FKGL: float
    DCRS: float

class AllScores(BaseModel):
    """Model for all evaluation scores."""
    original: ReadabilityScores
    generated: ReadabilityScores

class GenerateResponse(BaseModel):
    """The standard success response model."""
    status: str
    pls: str
    scores: AllScores
