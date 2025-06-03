from fastapi import HTTPException
from typing import List
from models.schemas import EduCert
import hashlib
import time

# In-memory store for demo (should be replaced by blockchain or persistent storage)
educert_db = {}
revocation_registry = set()

def sign_with_school_key(data: str) -> str:
    # Giả lập ký số bằng khóa trường (thực tế dùng private key)
    return hashlib.sha256(("school_secret" + data).encode()).hexdigest()

def verify_bls_signature(data: str, signature: str) -> bool:
    # Giả lập xác thực chữ ký BLS (thực tế dùng thuật toán BLS)
    expected = sign_with_school_key(data)
    return signature == expected

class EduCertService:
    def issue_certificate(self, cert_data: EduCert) -> dict:
        cert_dict = cert_data.dict()
        cert_dict.pop('id', None)
        cert_str = str(cert_dict)
        cert_hash = hashlib.sha256(cert_str.encode()).hexdigest()
        cert_data.id = cert_hash
        cert_data.signature = sign_with_school_key(cert_str)
        cert_data.issued_at = int(time.time())
        cert_data.revoked = False
        educert_db[cert_hash] = cert_data
        return {
            "credential_id": cert_hash,
            "issued_at": cert_data.issued_at,
            "signature": cert_data.signature
        }

    def revoke_certificate(self, credential_id: str) -> dict:
        cert = educert_db.get(credential_id)
        if not cert:
            raise HTTPException(status_code=404, detail="Credential not found")
        cert.revoked = True
        educert_db[credential_id] = cert
        revocation_registry.add(credential_id)
        return {"message": f"Credential {credential_id} revoked successfully"}

    def get_certificate(self, credential_id: str) -> dict:
        cert = educert_db.get(credential_id)
        if not cert:
            raise HTTPException(status_code=404, detail="Credential not found")
        return cert.dict()

    def list_certificates(self) -> List[dict]:
        return [cert.dict() for cert in educert_db.values()]

    def verify_certificate(self, cert_data: EduCert) -> dict:
        cert_dict = cert_data.dict()
        cert_dict.pop('id', None)
        cert_str = str(cert_dict)
        cert_hash = hashlib.sha256(cert_str.encode()).hexdigest()
        cert = educert_db.get(cert_hash)
        valid = (
            cert is not None and
            not cert.revoked and
            verify_bls_signature(cert_str, cert.signature)
        )
        return {
            "valid": valid,
            "credential_id": cert_hash,
            "revoked": cert.revoked if cert else None,
            "signature_valid": verify_bls_signature(cert_str, cert.signature) if cert else False
        }

    def is_revoked(self, credential_id: str) -> bool:
        return credential_id in revocation_registry