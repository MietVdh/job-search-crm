from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import get_session
from .crud import get_job_postings
from .schemas import JobPostingResponse

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, Career CRM!"}


@app.get("/job-postings", response_model=list[JobPostingResponse])
def job_postings(session: Session = Depends(get_session)):
    return get_job_postings(session)