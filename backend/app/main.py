from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .database import get_session
from .crud import get_job_postings, create_job_posting, DuplicateJobPostingError
from .schemas import JobPostingResponse, JobPostingCreate

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, Career CRM!"}


@app.get("/job-postings", response_model=list[JobPostingResponse])
def job_postings(session: Session = Depends(get_session)):
    return get_job_postings(session)


@app.post(
    "/job-postings",
    response_model = JobPostingResponse,
    status_code=status.HTTP_201_CREATED
    )
def create_job(job: JobPostingCreate, session: Session = Depends(get_session)):
    try:
        return create_job_posting(session, job)
    except DuplicateJobPostingError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A job posting with that URL already exists."
        )


