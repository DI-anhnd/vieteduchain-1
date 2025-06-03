from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

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