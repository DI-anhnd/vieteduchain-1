from fastapi import HTTPException
from typing import List
from models.schemas import EduCertCreate, EduCertResponse
from core.internal.modules.educert import EduCertModule

class EduCertService:
    def __init__(self):
        self.educert_module = EduCertModule()

    def issue_certificate(self, cert_data: EduCertCreate) -> EduCertResponse:
        try:
            cert_id = self.educert_module.issue(cert_data)
            return EduCertResponse(cert_id=cert_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def revoke_certificate(self, cert_id: str) -> None:
        try:
            self.educert_module.revoke(cert_id)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_certificate(self, cert_id: str) -> EduCertResponse:
        cert = self.educert_module.get(cert_id)
        if not cert:
            raise HTTPException(status_code=404, detail="Certificate not found")
        return cert

    def list_certificates(self) -> List[EduCertResponse]:
        return self.educert_module.list_all()