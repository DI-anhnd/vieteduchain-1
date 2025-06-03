from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from services.eduadmission_service import EduAdmissionService

router = APIRouter()

class SeatNFT(BaseModel):
    id: str
    candidate_hash: str
    score: float

class AdmissionResponse(BaseModel):
    message: str
    seat_nfts: List[SeatNFT]

@router.post("/admissions", response_model=AdmissionResponse)
async def create_admission(seat_nft: SeatNFT):
    # Logic to create admission and mint Seat-NFT
    return AdmissionResponse(message="Admission created successfully", seat_nfts=[seat_nft])

@router.get("/admissions/{candidate_hash}", response_model=AdmissionResponse)
async def get_admission(candidate_hash: str):
    # Logic to retrieve admission details
    seat_nfts = []  # Fetch seat NFTs associated with the candidate_hash
    return AdmissionResponse(message="Admission details retrieved successfully", seat_nfts=seat_nfts)