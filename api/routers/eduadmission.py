from fastapi import APIRouter, HTTPException, Form, Body
from pydantic import BaseModel
from typing import List
from services.eduadmission_service import EduAdmissionService, EduMarketService

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

@router.post("/admission/mint-seat-nft")
async def mint_seat_nft(university: str = Form(...), quota: int = Form(...)):
    return EduAdmissionService.mint_seat_nft(university, quota)

@router.post("/admission/burn-seat-nft")
async def burn_seat_nft(nft_id: str = Form(...)):
    return EduAdmissionService.burn_seat_nft(nft_id)

@router.post("/admission/push-score")
async def push_score(candidate_hash: str = Form(...), score: float = Form(...)):
    return EduAdmissionService.push_score(candidate_hash, score)

@router.post("/admission/matching-engine")
async def matching_engine(applications: List[dict]):
    return EduAdmissionService.run_matching_engine(applications)

# EduMarket
@router.post("/edumarket/mint-course-nft")
async def mint_course_nft(lecturer: str = Form(...), course_name: str = Form(...)):
    return EduMarketService.mint_course_nft(lecturer, course_name)

@router.post("/edumarket/pay-course")
async def pay_course(student: str = Form(...), nft_id: str = Form(...), amount: float = Form(...)):
    return EduMarketService.pay_course(student, nft_id, amount)

# CRUD Seat-NFT endpoints
@router.post("/eduadmission/seat-nft", status_code=201)
async def create_seat_nft(data: dict = Body(...)):
    # Tạo mới Seat-NFT
    import uuid
    nft_id = str(uuid.uuid4())
    from services.eduadmission_service import seat_nft_db
    seat_nft_db[nft_id] = {"id": nft_id, **data}
    return {"nft_id": nft_id, **data}

@router.get("/eduadmission/seat-nft/{nft_id}")
async def get_seat_nft(nft_id: str):
    from services.eduadmission_service import seat_nft_db
    nft = seat_nft_db.get(nft_id)
    if not nft:
        raise HTTPException(status_code=404, detail="Seat-NFT not found")
    return {"id": nft_id, **nft}

@router.put("/eduadmission/seat-nft/{nft_id}")
async def update_seat_nft(nft_id: str, data: dict = Body(...)):
    from services.eduadmission_service import seat_nft_db
    nft = seat_nft_db.get(nft_id)
    if not nft:
        raise HTTPException(status_code=404, detail="Seat-NFT not found")
    nft.update(data)
    seat_nft_db[nft_id] = nft
    return {"id": nft_id, **nft}

@router.delete("/eduadmission/seat-nft/{nft_id}", status_code=204)
async def delete_seat_nft(nft_id: str):
    from services.eduadmission_service import seat_nft_db
    if nft_id in seat_nft_db:
        del seat_nft_db[nft_id]
        return
    raise HTTPException(status_code=404, detail="Seat-NFT not found")

@router.get("/eduadmission/seat-nfts")
async def list_seat_nfts():
    from services.eduadmission_service import seat_nft_db
    return list(seat_nft_db.values())