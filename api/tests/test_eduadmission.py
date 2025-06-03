import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_seat_nft():
    response = client.post("/eduadmission/seat-nft", json={"data": "sample_data"})
    assert response.status_code == 201
    assert "nft_id" in response.json()
    global created_nft_id
    created_nft_id = response.json()["nft_id"]

def test_get_seat_nft():
    test_create_seat_nft()
    response = client.get(f"/eduadmission/seat-nft/{created_nft_id}")
    assert response.status_code == 200
    assert "data" in response.json()

def test_update_seat_nft():
    test_create_seat_nft()
    response = client.put(f"/eduadmission/seat-nft/{created_nft_id}", json={"data": "updated_data"})
    assert response.status_code == 200
    assert response.json()["data"] == "updated_data"

def test_delete_seat_nft():
    test_create_seat_nft()
    response = client.delete(f"/eduadmission/seat-nft/{created_nft_id}")
    assert response.status_code == 204

def test_get_all_seat_nfts():
    response = client.get("/eduadmission/seat-nfts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_mint_and_burn_seat_nft():
    response = client.post("/admission/mint-seat-nft", data={"university": "ABC", "quota": 2})
    assert response.status_code == 200
    nfts = response.json()
    assert len(nfts) == 2
    nft_id = nfts[0]["nft_id"]
    burn_res = client.post("/admission/burn-seat-nft", data={"nft_id": nft_id})
    assert burn_res.status_code == 200
    assert burn_res.json()["status"] == "burned"

def test_push_score():
    candidate_hash = "hash123"
    response = client.post("/admission/push-score", data={"candidate_hash": candidate_hash, "score": 9.5})
    assert response.status_code == 200
    assert response.json()["score"] == 9.5

def test_matching_engine():
    # Mint 2 seats
    mint_res = client.post("/admission/mint-seat-nft", data={"university": "DEF", "quota": 2})
    nfts = mint_res.json()
    apps = [
        {"candidate_hash": "c1", "score": 8.0, "nft_id": nfts[0]["nft_id"]},
        {"candidate_hash": "c2", "score": 9.0, "nft_id": nfts[1]["nft_id"]},
        {"candidate_hash": "c3", "score": 7.5, "nft_id": nfts[0]["nft_id"]}
    ]
    import json
    res = client.post("/admission/matching-engine", json=apps)
    assert res.status_code == 200
    data = res.json()
    assert "match_id" in data
    assert len(data["result"]) == 2

def test_mint_course_nft_and_pay():
    mint_res = client.post("/edumarket/mint-course-nft", data={"lecturer": "GV1", "course_name": "Blockchain 101"})
    assert mint_res.status_code == 200
    nft_id = mint_res.json()["nft_id"]
    pay_res = client.post("/edumarket/pay-course", data={"student": "S1", "nft_id": nft_id, "amount": 1000})
    assert pay_res.status_code == 200
    data = pay_res.json()
    assert data["fee"] == 20.0
    assert data["net"] == 980.0