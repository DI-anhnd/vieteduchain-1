from pydantic import BaseModel
from typing import List, Optional

class EduCert(BaseModel):
    id: str = ""
    student_id: str
    institution_id: str
    credential_type: str
    issued_date: str
    expiration_date: Optional[str] = None
    revoked: bool = False
    signature: Optional[str] = None
    issued_at: Optional[int] = None

class EduID(BaseModel):
    id: str
    did: str
    public_key: str
    services: List[str]

class EduPay(BaseModel):
    transaction_id: str
    student_id: str
    amount: float
    currency: str
    timestamp: str
    status: str

class ResearchLedger(BaseModel):
    id: str
    document_hash: str
    authors: List[str]
    publication_date: str
    doi: str

class EduAdmission(BaseModel):
    id: str
    seat_nft: str
    candidate_id: str
    score: float
    admission_status: str
    timestamp: str

class EduIDSchema(EduID):
    pass

class EduIDCreateSchema(BaseModel):
    did: str
    public_key: str
    services: List[str]

class Admission(BaseModel):
    id: str
    seat_nft: str
    candidate_id: str
    score: float
    admission_status: str
    timestamp: str

class SeatNFT(BaseModel):
    id: str
    owner: str
    metadata: str

class Score(BaseModel):
    candidate_id: str
    value: float