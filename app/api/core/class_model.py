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
    relevance_bertscore_f1: float
    factuality_alignscore: float
    readability: ReadabilityScores

class GenerateResponse(BaseModel):
    """The standard success response model."""
    status: str
    pls: str
    scores: AllScores

class ErrorResponse(BaseModel):
    """The standard error response model."""
    status: str
    message: str