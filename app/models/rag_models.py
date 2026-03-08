from pydantic import BaseModel

class QueryRequest(BaseModel):
    """Model untuk permintaan yang masuk ke endpoint /ask."""
    question: str

class QueryResponse(BaseModel):
    """Model untuk respons yang dikirim kembali dari endpoint /ask."""
    answer: str
