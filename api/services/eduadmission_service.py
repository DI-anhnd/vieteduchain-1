from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import Admission, SeatNFT, Score
import hashlib
import uuid
import time

router = APIRouter()

# In-memory store for demo (should be replaced by blockchain or persistent storage)
seat_nft_db = {}
score_oracle_db = {}
matching_result_db = {}
course_nft_db = {}
edumarket_tx_db = {}

@router.post("/admissions/", response_model=Admission)
async def create_admission(admission: Admission):
    # Logic to create a new admission record
    pass

@router.get("/admissions/{admission_id}", response_model=Admission)
async def read_admission(admission_id: int):
    # Logic to retrieve an admission record by ID
    pass

@router.get("/admissions/", response_model=List[Admission])
async def read_admissions(skip: int = 0, limit: int = 10):
    # Logic to retrieve a list of admissions
    pass

@router.post("/seat-nfts/", response_model=SeatNFT)
async def create_seat_nft(seat_nft: SeatNFT):
    # Logic to mint a new Seat NFT
    pass

@router.get("/seat-nfts/{nft_id}", response_model=SeatNFT)
async def read_seat_nft(nft_id: int):
    # Logic to retrieve a Seat NFT by ID
    pass

@router.post("/scores/", response_model=Score)
async def submit_score(score: Score):
    # Logic to submit a score for an admission
    pass

@router.get("/scores/{candidate_hash}", response_model=Score)
async def get_score(candidate_hash: str):
    # Logic to retrieve a score by candidate hash
    pass

# CRUD Seat-NFT logic for REST endpoints

def create_seat_nft(data: dict) -> dict:
    nft_id = str(uuid.uuid4())
    seat_nft_db[nft_id] = {"id": nft_id, **data}
    return {"nft_id": nft_id, **data}

def get_seat_nft(nft_id: str) -> dict:
    nft = seat_nft_db.get(nft_id)
    if not nft:
        raise HTTPException(status_code=404, detail="Seat-NFT not found")
    return {"id": nft_id, **nft}

def update_seat_nft(nft_id: str, data: dict) -> dict:
    nft = seat_nft_db.get(nft_id)
    if not nft:
        raise HTTPException(status_code=404, detail="Seat-NFT not found")
    nft.update(data)
    seat_nft_db[nft_id] = nft
    return {"id": nft_id, **nft}

def delete_seat_nft(nft_id: str):
    if nft_id in seat_nft_db:
        del seat_nft_db[nft_id]
        return
    raise HTTPException(status_code=404, detail="Seat-NFT not found")

def list_seat_nfts() -> list:
    return list(seat_nft_db.values())

class EduAdmissionService:
    @staticmethod
    def mint_seat_nft(university: str, quota: int) -> list:
        # Mint quota NFTs for university
        nfts = []
        for _ in range(quota):
            nft_id = str(uuid.uuid4())
            seat_nft_db[nft_id] = {
                "nft_id": nft_id,
                "university": university,
                "status": "available"
            }
            nfts.append(seat_nft_db[nft_id])
        return nfts

    @staticmethod
    def burn_seat_nft(nft_id: str) -> dict:
        nft = seat_nft_db.get(nft_id)
        if not nft:
            return {"error": "NFT not found"}
        nft["status"] = "burned"
        return {"nft_id": nft_id, "status": "burned"}

    @staticmethod
    def push_score(candidate_hash: str, score: float) -> dict:
        score_oracle_db[candidate_hash] = score
        return {"candidate_hash": candidate_hash, "score": score}

    @staticmethod
    def run_matching_engine(applications: list) -> dict:
        # Giả lập Deferred-Acceptance: chọn top score cho mỗi seat
        # applications: [{"candidate_hash", "score", "nft_id"}]
        filled = set()
        result = []
        for app in sorted(applications, key=lambda x: -x["score"]):
            nft_id = app["nft_id"]
            if nft_id not in filled and seat_nft_db.get(nft_id, {}).get("status") == "available":
                filled.add(nft_id)
                result.append(app)
                seat_nft_db[nft_id]["status"] = "matched"
        match_id = str(uuid.uuid4())
        matching_result_db[match_id] = result
        return {"match_id": match_id, "result": result}

# EduMarket
class EduMarketService:
    @staticmethod
    def mint_course_nft(lecturer: str, course_name: str) -> dict:
        nft_id = str(uuid.uuid4())
        course_nft_db[nft_id] = {
            "nft_id": nft_id,
            "lecturer": lecturer,
            "course_name": course_name,
            "timestamp": int(time.time())
        }
        return course_nft_db[nft_id]

    @staticmethod
    def pay_course(student: str, nft_id: str, amount: float) -> dict:
        # 2% fee to scholarship fund
        fee = round(amount * 0.02, 2)
        net = amount - fee
        tx_id = str(uuid.uuid4())
        edumarket_tx_db[tx_id] = {
            "student": student,
            "nft_id": nft_id,
            "amount": amount,
            "fee": fee,
            "net": net,
            "timestamp": int(time.time())
        }
        return {"tx_id": tx_id, "fee": fee, "net": net}