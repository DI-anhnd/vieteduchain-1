import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from components import (
    educert_api,
    eduid_view,
    edupay_view,
    researchledger_view,
    eduadmission_view,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(educert_api.router, prefix="/educert", tags=["EduCert"])
app.include_router(eduid_view.router, prefix="/eduid", tags=["EduID"])
app.include_router(edupay_view.router, prefix="/edupay", tags=["EduPay"])
app.include_router(researchledger_view.router, prefix="/researchledger", tags=["ResearchLedger"])
app.include_router(eduadmission_view.router, prefix="/eduadmission", tags=["EduAdmission"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the VietEduChain GUI API!"}