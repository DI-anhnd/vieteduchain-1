import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_register_hash():
    response = client.post("/researchledger/register", json={"data": "sample_data"})
    assert response.status_code == 200
    assert "hash" in response.json()

def test_plagiarism_check():
    response = client.post("/researchledger/plagiarism-check", json={"hash": "sample_hash"})
    assert response.status_code == 200
    assert "is_plagiarized" in response.json()

def test_get_doi_nft():
    response = client.get("/researchledger/doi-nft/sample_doi")
    assert response.status_code == 200
    assert "doi" in response.json() and response.json()["doi"] == "sample_doi"

def test_bounty_submission():
    response = client.post("/researchledger/bounty", json={"hash": "sample_hash"})
    assert response.status_code == 200
    assert "bounty_id" in response.json()