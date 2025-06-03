from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
import hashlib
import uuid
import time

# Define the data model for ResearchLedger
class ResearchRecord(BaseModel):
    id: str
    title: str
    authors: List[str]
    doi: str
    timestamp: str
    hash: str

class PlagiarismReport(BaseModel):
    record_id: str
    is_plagiarized: bool
    similarity_score: float

# Initialize the router
router = APIRouter()

# In-memory storage for research records (for demonstration purposes)
research_records = {}
plagiarism_reports = {}

@router.post("/research", response_model=ResearchRecord)
async def create_research_record(record: ResearchRecord):
    if record.id in research_records:
        raise HTTPException(status_code=400, detail="Record already exists")
    research_records[record.id] = record
    return record

@router.get("/research/{record_id}", response_model=ResearchRecord)
async def get_research_record(record_id: str):
    record = research_records.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@router.post("/plagiarism", response_model=PlagiarismReport)
async def report_plagiarism(report: PlagiarismReport):
    plagiarism_reports[report.record_id] = report
    return report

@router.get("/plagiarism/{record_id}", response_model=PlagiarismReport)
async def get_plagiarism_report(record_id: str):
    report = plagiarism_reports.get(record_id)
    if not report:
        raise HTTPException(status_code=404, detail="Plagiarism report not found")
    return report

# In-memory store for demo (should be replaced by blockchain or persistent storage)
ledger_db = {}
doi_nft_db = {}
bounty_pool = {}

class ResearchLedgerService:
    @staticmethod
    def register_hash(file_bytes: bytes) -> dict:
        # Data Fingerprint: SHA-256 hash
        file_hash = hashlib.sha256(file_bytes).hexdigest()
        msg_id = str(uuid.uuid4())
        ledger_db[msg_id] = {
            "hash": file_hash,
            "timestamp": int(time.time())
        }
        return {"msg_id": msg_id, "hash": file_hash}

    @staticmethod
    def mint_doi_nft(doi: str, cid: str, authors: list) -> dict:
        nft_id = str(uuid.uuid4())
        nft = {
            "nft_id": nft_id,
            "doi": doi,
            "cid": cid,
            "timestamp": int(time.time()),
            "authors": authors
        }
        doi_nft_db[nft_id] = nft
        return nft

    @staticmethod
    def submit_plagiarism_bounty(hash1: str, hash2: str, submitter: str) -> dict:
        # Nếu hash1 == hash2 thì thưởng token RESEARCH cho submitter
        if hash1 == hash2:
            bounty_id = str(uuid.uuid4())
            bounty_pool[bounty_id] = {
                "submitter": submitter,
                "hash": hash1,
                "reward": 100,  # fixed for demo
                "timestamp": int(time.time())
            }
            return {"bounty_id": bounty_id, "reward": 100, "status": "rewarded"}
        return {"status": "not plagiarism"}