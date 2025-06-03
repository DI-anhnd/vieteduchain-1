import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_create_payment():
    response = client.post("/edupay/create", json={"amount": 1000, "currency": "eVND"})
    assert response.status_code == 201
    assert response.json() == {"message": "Payment created successfully", "payment_id": response.json()["payment_id"]}

def test_get_payment_status():
    payment_id = "test_payment_id"
    response = client.get(f"/edupay/status/{payment_id}")
    assert response.status_code == 200
    assert "status" in response.json()

def test_invalid_payment_creation():
    response = client.post("/edupay/create", json={"amount": -1000, "currency": "eVND"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid payment amount"}

def test_payment_not_found():
    payment_id = "invalid_payment_id"
    response = client.get(f"/edupay/status/{payment_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}