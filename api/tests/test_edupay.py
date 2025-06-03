import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_payment():
    response = client.post("/edupay/create", json={"student_id": "test_student", "amount": 1000, "currency": "eVND"})
    assert response.status_code == 201
    assert response.json()["message"] == "Payment created successfully"
    assert "payment_id" in response.json()


def test_get_payment_status():
    # Tạo payment trước để lấy payment_id
    response = client.post("/edupay/create", json={"student_id": "test_student", "amount": 1000, "currency": "eVND"})
    assert response.status_code == 201
    payment_id = response.json()["payment_id"]
    response = client.get(f"/edupay/status/{payment_id}")
    assert response.status_code == 200
    assert "status" in response.json()

def test_invalid_payment_creation():
    response = client.post("/edupay/create", json={"student_id": "test_student", "amount": -1000, "currency": "eVND"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid payment amount"}

def test_payment_not_found():
    payment_id = "invalid_payment_id"
    response = client.get(f"/edupay/status/{payment_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "Payment not found"}

def test_stablecoin_mint():
    from services.edupay_service import EduPayService
    result = EduPayService.mint_stablecoin("student1", 1000)
    assert result["student_id"] == "student1"
    assert result["amount"] == 1000
    assert result["currency"] == "eVND"
    assert "txid" in result

def test_create_and_release_escrow():
    from services.edupay_service import EduPayService
    escrow_id = EduPayService.create_escrow("payer1", "school1", 5000)
    assert escrow_id
    # Chưa có proof thì chưa release
    res = EduPayService.release_escrow(escrow_id, False)
    assert res["status"] == "pending"
    # Có proof thì release
    res2 = EduPayService.release_escrow(escrow_id, True)
    assert res2["status"] == "released"

def test_oracle_price():
    from services.edupay_service import EduPayService
    price1 = EduPayService.get_oracle_price()
    assert "eVND/USDC" in price1
    assert abs(price1["eVND/USDC"] - 1.0) < 0.01  # Giá dao động nhỏ quanh 1.0
    # Gọi lại sau 16s sẽ tự update
    import time as t
    t.sleep(16)
    price2 = EduPayService.get_oracle_price()
    assert "eVND/USDC" in price2
    assert abs(price2["eVND/USDC"] - 1.0) < 0.01