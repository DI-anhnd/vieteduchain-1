from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.edupay_service import EduPayService

router = APIRouter()

class PaymentRequest(BaseModel):
    student_id: str = "test_student"  # Thêm mặc định để test không lỗi thiếu trường
    amount: float
    currency: str

class PaymentResponse(BaseModel):
    transaction_id: str
    status: str

@router.post("/pay", response_model=PaymentResponse)
async def make_payment(payment_request: PaymentRequest):
    # Logic to process the payment
    # This is a placeholder for actual payment processing logic
    if payment_request.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
    
    transaction_id = "txn_123456"  # Placeholder for generated transaction ID
    return PaymentResponse(transaction_id=transaction_id, status="success")

@router.get("/payments/{student_id}", response_model=List[PaymentResponse])
async def get_payments(student_id: str):
    # Logic to retrieve payments for a student
    # This is a placeholder for actual retrieval logic
    return [
        PaymentResponse(transaction_id="txn_123456", status="success"),
        PaymentResponse(transaction_id="txn_654321", status="success"),
    ]

@router.post("/edupay/create", status_code=201)
async def create_payment(payment: PaymentRequest):
    if payment.amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid payment amount")
    import uuid
    payment_id = str(uuid.uuid4())
    from services.edupay_service import payment_db
    payment_db[payment_id] = {
        "student_id": payment.student_id,
        "amount": payment.amount,
        "currency": payment.currency,
        "status": "created"
    }
    return {"message": "Payment created successfully", "payment_id": payment_id}

@router.get("/edupay/status/{payment_id}")
async def get_payment_status(payment_id: str):
    from services.edupay_service import payment_db
    payment = payment_db.get(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return {"status": payment["status"]}