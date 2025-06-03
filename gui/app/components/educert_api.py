from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Certificate(BaseModel):
    id: str
    name: str
    issued_by: str
    issued_to: str
    date_issued: str

class CertificateResponse(BaseModel):
    success: bool
    message: str
    data: Certificate = None

@router.post("/issue", response_model=CertificateResponse)
async def issue_certificate(cert: Certificate):
    # Logic to issue a certificate
    return CertificateResponse(success=True, message="Certificate issued", data=cert)

@router.get("/list", response_model=List[Certificate])
async def list_certificates():
    # Logic to list certificates
    return []

@router.delete("/revoke/{cert_id}", response_model=CertificateResponse)
async def revoke_certificate(cert_id: str):
    # Logic to revoke a certificate
    return CertificateResponse(success=True, message=f"Certificate {cert_id} revoked")
