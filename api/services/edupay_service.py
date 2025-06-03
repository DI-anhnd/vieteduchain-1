from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import random
import time

router = APIRouter()

class PaymentRequest(BaseModel):
    student_id: str
    amount: float
    currency: str = "eVND"

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str

@router.post("/edupay/pay", response_model=PaymentResponse)
async def pay_tuition(payment_request: PaymentRequest):
    # Logic to process the payment
    # This is a placeholder for actual payment processing logic
    if payment_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    transaction_id = "txn_123456"  # This should be generated dynamically
    status = "success"  # This should reflect the actual payment status

    return PaymentResponse(transaction_id=transaction_id, status=status)

@router.get("/edupay/status/{transaction_id}", response_model=PaymentResponse)
async def get_payment_status(transaction_id: str):
    # Logic to retrieve payment status
    # This is a placeholder for actual status retrieval logic
    if transaction_id != "txn_123456":
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return PaymentResponse(transaction_id=transaction_id, status="success")

# Dummy class to fix import error for legacy code
class EduPayService:
    pass

# In-memory store for demo (should be replaced by blockchain or persistent storage)
payment_db = {}
escrow_db = {}
oracle_price = {"eVND/USDC": 1.00, "last_update": time.time()}

# --- Stablecoin VNĐ (eVND) logic ---
class Stablecoin:
    @staticmethod
    def mint(student_id: str, amount: float) -> dict:
        # Giả lập phát hành eVND cho student_id
        return {"student_id": student_id, "amount": amount, "currency": "eVND", "txid": str(uuid.uuid4())}

# --- Escrow Contract logic ---
def create_escrow(payer: str, school: str, amount: float) -> str:
    escrow_id = str(uuid.uuid4())
    escrow_db[escrow_id] = {
        "payer": payer,
        "school": school,
        "amount": amount,
        "released": False
    }
    return escrow_id

def release_escrow(escrow_id: str, proof_of_enrollment: bool) -> dict:
    escrow = escrow_db.get(escrow_id)
    if not escrow:
        raise HTTPException(status_code=404, detail="Escrow not found")
    if proof_of_enrollment and not escrow["released"]:
        escrow["released"] = True
        return {"status": "released", "escrow_id": escrow_id}
    return {"status": "pending", "escrow_id": escrow_id}

# --- Oracle VNĐ/USDC logic ---
def update_oracle_price():
    # Giả lập cập nhật giá từ Band⸱Relay, mỗi lần gọi sẽ random trong biên độ ±0.25%
    base = 1.00
    delta = base * 0.0025
    new_price = base + random.uniform(-delta, delta)
    oracle_price["eVND/USDC"] = round(new_price, 6)
    oracle_price["last_update"] = time.time()
    return oracle_price

def get_oracle_price() -> dict:
    # Nếu quá 15s thì tự động cập nhật lại
    if time.time() - oracle_price["last_update"] > 15:
        update_oracle_price()
    return {"eVND/USDC": oracle_price["eVND/USDC"], "last_update": oracle_price["last_update"]}

class EduPayService:
    @staticmethod
    def mint_stablecoin(student_id: str, amount: float) -> dict:
        return Stablecoin.mint(student_id, amount)

    @staticmethod
    def create_escrow(payer: str, school: str, amount: float) -> str:
        return create_escrow(payer, school, amount)

    @staticmethod
    def release_escrow(escrow_id: str, proof_of_enrollment: bool) -> dict:
        return release_escrow(escrow_id, proof_of_enrollment)

    @staticmethod
    def get_oracle_price() -> dict:
        return get_oracle_price()