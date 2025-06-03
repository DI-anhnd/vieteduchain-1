from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

class ResearchRecord(BaseModel):
    id: str
    title: str
    authors: List[str]
    doi: str
    timestamp: str

@router.get("/researchledger", response_model=List[ResearchRecord])
async def get_research_records():
    # Logic to retrieve research records from the backend
    return []

@router.post("/researchledger", response_model=ResearchRecord)
async def add_research_record(record: ResearchRecord):
    # Logic to add a new research record to the backend
    return record

@router.delete("/researchledger/{record_id}", response_model=dict)
async def delete_research_record(record_id: str):
    # Logic to delete a research record from the backend
    return {"message": "Record deleted successfully"}