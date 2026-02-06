from fastapi import FastAPI, Depends, Security
from core.auth import verify_api_key

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "Fit-Gap API"}

# Protected dummy endpoints for auth testing
@app.post("/resumes", dependencies=[Depends(verify_api_key)])
def create_resume():
    return {"message": "Success"}

@app.post("/postings", dependencies=[Depends(verify_api_key)])
def create_posting():
    return {"message": "Success"}
