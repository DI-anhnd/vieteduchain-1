from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class AdmissionSeat(BaseModel):
    seat_id: str
    status: str

class AdmissionResponse(BaseModel):
    seats: List[AdmissionSeat]

@router.get("/admission/seats", response_model=AdmissionResponse)
async def get_admission_seats():
    # Placeholder for fetching admission seats
    return AdmissionResponse(seats=[
        AdmissionSeat(seat_id="1", status="available"),
        AdmissionSeat(seat_id="2", status="occupied"),
    ])

@router.post("/admission/confirm")
async def confirm_admission(seat_id: str):
    # Placeholder for confirming admission
    return {"message": f"Admission confirmed for seat {seat_id}"}