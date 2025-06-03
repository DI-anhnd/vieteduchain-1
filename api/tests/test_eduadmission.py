import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_seat_nft():
    response = client.post("/eduadmission/seat-nft", json={"data": "sample_data"})
    assert response.status_code == 201
    assert "nft_id" in response.json()

def test_get_seat_nft():
    response = client.get("/eduadmission/seat-nft/{nft_id}")
    assert response.status_code == 200
    assert "data" in response.json()

def test_update_seat_nft():
    response = client.put("/eduadmission/seat-nft/{nft_id}", json={"data": "updated_data"})
    assert response.status_code == 200
    assert response.json()["data"] == "updated_data"

def test_delete_seat_nft():
    response = client.delete("/eduadmission/seat-nft/{nft_id}")
    assert response.status_code == 204

def test_get_all_seat_nfts():
    response = client.get("/eduadmission/seat-nfts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)