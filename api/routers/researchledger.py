from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
from services.researchledger_service import ResearchLedgerService

router = APIRouter()

class DataFingerprint(BaseModel):
    hash: str

class DOI_NFT(BaseModel):
    doi: str
    metadata: dict

class PlagiarismBounty(BaseModel):
    hash: str
    proof: str

@router.post("/register_hash", response_model=DataFingerprint)
async def register_hash(data: DataFingerprint):
    # Logic to register the hash in the ResearchLedger
    return data

@router.post("/create_doi_nft", response_model=DOI_NFT)
async def create_doi_nft(data: DOI_NFT):
    # Logic to create a DOI NFT
    return data

@router.post("/report_plagiarism", response_model=PlagiarismBounty)
async def report_plagiarism(data: PlagiarismBounty):
    # Logic to report plagiarism
    return data

@router.get("/get_hash/{hash}", response_model=DataFingerprint)
async def get_hash(hash: str):
    # Logic to retrieve the hash from the ResearchLedger
    raise HTTPException(status_code=404, detail="Hash not found")

@router.post("/researchledger/register-hash")
async def register_hash(file: UploadFile = File(...)):
    file_bytes = await file.read()
    return ResearchLedgerService.register_hash(file_bytes)

@router.post("/researchledger/mint-doi-nft")
async def mint_doi_nft(doi: str = Form(...), cid: str = Form(...), authors: List[str] = Form(...)):
    return ResearchLedgerService.mint_doi_nft(doi, cid, authors)

@router.post("/researchledger/plagiarism-bounty")
async def submit_plagiarism_bounty(hash1: str = Form(...), hash2: str = Form(...), submitter: str = Form(...)):
    return ResearchLedgerService.submit_plagiarism_bounty(hash1, hash2, submitter)