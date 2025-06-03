import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app
from models.schemas import EduCert

client = TestClient(app)

sample_cert = {
    "id": "",  # Thêm id rỗng để khớp schema
    "student_id": "12345",
    "institution_id": "UNI-001",
    "credential_type": "Bachelor of Science",
    "issued_date": "2023-01-01",
    "expiration_date": None,
    "revoked": False
}

def test_issue_verifiable_credential():
    response = client.post("/edu-cert/issue", json=sample_cert)
    print(response.text)  # In chi tiết lỗi nếu có
    assert response.status_code == 200
    data = response.json()
    assert "credential_id" in data
    global issued_id
    issued_id = data["credential_id"]
    global issued_signature
    issued_signature = data["signature"]

def test_view_verifiable_credential():
    test_issue_verifiable_credential()
    response = client.get(f"/edu-cert/view/{issued_id}")
    print(response.text)
    assert response.status_code == 200
    cert = response.json()
    assert cert["id"] == issued_id
    assert cert["signature"] == issued_signature

def test_verify_verifiable_credential():
    test_issue_verifiable_credential()
    response = client.post("/edu-cert/verify", json=sample_cert)
    print(response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is True
    assert data["signature_valid"] is True
    assert data["revoked"] is False

def test_revoke_verifiable_credential():
    test_issue_verifiable_credential()
    response = client.post("/edu-cert/revoke", json={"credential_id": issued_id})
    print(response.text)
    assert response.status_code == 200
    assert "revoked" in response.json().get("message", "")
    # Sau khi revoke, verify phải trả về valid=False
    response = client.post("/edu-cert/verify", json=sample_cert)
    print(response.text)
    assert response.status_code == 200
    data = response.json()
    assert data["valid"] is False
    assert data["revoked"] is True
    assert data["signature_valid"] is True