from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel

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