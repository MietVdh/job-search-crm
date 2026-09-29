from fastapi import FastAPI, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from .database import get_session
from .crud import get_job_postings, create_job_posting, DuplicateJobPostingError, get_job_applications
from .schemas import ApplicationListItem, JobPostingResponse, JobPostingCreate, PaginatedResponse

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello, Career CRM!"}


@app.get("/job-postings", response_model=PaginatedResponse[JobPostingResponse])
def job_postings(
    page: Annotated[int, Query(ge=1)] = 1, 
    page_size: Annotated[int, Query(ge=1, le=50)] = 25,
    session: Session = Depends(get_session)
):
    offset = (page - 1) * page_size
    postings, total = get_job_postings(session, offset, page_size)

    return PaginatedResponse[JobPostingResponse](
        items=postings,
        page=page,
        page_size=page_size,
        total=total
    )


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



@app.get("/applications", response_model=PaginatedResponse[ApplicationListItem])
def get_applications(
    page: Annotated[int, Query(ge=1)] = 1, 
    page_size: Annotated[int, Query(ge=1, le=50)] = 25,
    session: Session = Depends(get_session)
):
    offset = (page - 1) * page_size
    applications, total = get_job_applications(session, offset, page_size)

    return PaginatedResponse[ApplicationListItem](
        items=applications,
        page=page,
        page_size=page_size,
        total=total
    )


