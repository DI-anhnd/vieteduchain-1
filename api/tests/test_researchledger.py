import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_hash():
    file_content = b"This is a test PDF file."
    response = client.post("/researchledger/register-hash", files={"file": ("test.pdf", file_content)})
    assert response.status_code == 200
    data = response.json()
    assert "hash" in data
    assert len(data["hash"]) == 64

def test_mint_doi_nft():
    response = client.post(
        "/researchledger/mint-doi-nft",
        data={"doi": "10.1234/abc", "cid": "cid123", "authors": ["Alice", "Bob"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["doi"] == "10.1234/abc"
    assert data["cid"] == "cid123"
    assert "nft_id" in data
    assert "authors" in data

def test_plagiarism_bounty():
    # Hash giống nhau sẽ được thưởng
    hash_val = "a" * 64
    response = client.post(
        "/researchledger/plagiarism-bounty",
        data={"hash1": hash_val, "hash2": hash_val, "submitter": "alice"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rewarded"
    assert data["reward"] == 100
    # Hash khác nhau sẽ không thưởng
    response = client.post(
        "/researchledger/plagiarism-bounty",
        data={"hash1": hash_val, "hash2": "b" * 64, "submitter": "bob"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "not plagiarism"