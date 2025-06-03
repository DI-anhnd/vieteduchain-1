from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class Payment(BaseModel):
    student_id: str
    amount: float
    currency: str

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str

@router.post("/edupay/pay", response_model=PaymentResponse)
async def make_payment(payment: Payment):
    # Logic to process the payment
    transaction_id = "txn_123456"  # Placeholder for transaction ID
    status = "success"  # Placeholder for payment status
    return PaymentResponse(transaction_id=transaction_id, status=status)

@router.get("/edupay/history/{student_id}", response_model=List[PaymentResponse])
async def get_payment_history(student_id: str):
    # Logic to retrieve payment history
    return [
        PaymentResponse(transaction_id="txn_123456", status="success"),
        PaymentResponse(transaction_id="txn_654321", status="failed"),
    ]