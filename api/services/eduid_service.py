from fastapi import APIRouter, HTTPException
from typing import List
from models.schemas import EduIDSchema, EduIDCreateSchema

router = APIRouter()

# In-memory storage for EduID records (for demonstration purposes)
eduid_storage = {}

@router.post("/eduid/", response_model=EduIDSchema)
async def create_eduid(eduid: EduIDCreateSchema):
    if eduid.id in eduid_storage:
        raise HTTPException(status_code=400, detail="EduID already exists")
    
    eduid_storage[eduid.id] = eduid
    return eduid

@router.get("/eduid/{eduid_id}", response_model=EduIDSchema)
async def read_eduid(eduid_id: str):
    if eduid_id not in eduid_storage:
        raise HTTPException(status_code=404, detail="EduID not found")
    
    return eduid_storage[eduid_id]

@router.get("/eduid/", response_model=List[EduIDSchema])
async def list_eduid():
    return list(eduid_storage.values())

# Dummy class to fix import error for legacy code
class EduIDService:
    pass