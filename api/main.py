from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import educert, eduid, edupay, researchledger, eduadmission

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(educert.router)
app.include_router(eduid.router)
app.include_router(edupay.router)
app.include_router(researchledger.router)
app.include_router(eduadmission.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the VietEduChain API"}