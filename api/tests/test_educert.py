import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_issue_verifiable_credential():
    response = client.post("/edu-cert/issue", json={
        "student_id": "12345",
        "credential_data": {
            "degree": "Bachelor of Science",
            "major": "Computer Science",
            "issued_date": "2023-01-01"
        }
    })
    assert response.status_code == 200
    assert "credential_id" in response.json()

def test_revoke_verifiable_credential():
    response = client.post("/edu-cert/revoke", json={
        "credential_id": "credential_id_example"
    })
    assert response.status_code == 200
    assert response.json() == {"message": "Credential revoked successfully"}

def test_view_verifiable_credential():
    response = client.get("/edu-cert/view/credential_id_example")
    assert response.status_code == 200
    assert response.json()["credential_id"] == "credential_id_example"