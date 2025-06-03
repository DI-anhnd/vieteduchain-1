from fastapi import APIRouter, HTTPException
from services.eduid_service import EduIDService
from models.schemas import EduIDSchema

router = APIRouter()

@router.post("/eduid/create", response_model=EduIDSchema)
async def create_eduid(eduid: EduIDSchema):
    try:
        return await EduIDService.create_eduid(eduid)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/eduid/{eduid_id}", response_model=EduIDSchema)
async def get_eduid(eduid_id: str):
    try:
        return await EduIDService.get_eduid(eduid_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/eduid/{eduid_id}")
async def delete_eduid(eduid_id: str):
    try:
        await EduIDService.delete_eduid(eduid_id)
        return {"detail": "EduID deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))