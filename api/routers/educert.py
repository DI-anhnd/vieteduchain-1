from fastapi import APIRouter, HTTPException
from models.schemas import EduCert
from services.educert_service import EduCertService

router = APIRouter()
educert_service = EduCertService()

@router.post("/edu-cert/issue")
def issue_credential(cert: EduCert):
    return educert_service.issue_certificate(cert)

@router.post("/edu-cert/revoke")
def revoke_credential(data: dict):
    credential_id = data.get("credential_id")
    if not credential_id:
        raise HTTPException(status_code=400, detail="Missing credential_id")
    return educert_service.revoke_certificate(credential_id)

@router.get("/edu-cert/view/{credential_id}")
def get_credential(credential_id: str):
    return educert_service.get_certificate(credential_id)

@router.post("/edu-cert/verify")
def verify_credential(cert: EduCert):
    return educert_service.verify_certificate(cert)

@router.get("/edu-cert/list")
def list_credentials():
    return educert_service.list_certificates()