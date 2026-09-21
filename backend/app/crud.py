from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from backend.app.models import JobPosting
from .schemas import JobPostingCreate


class DuplicateJobPostingError(Exception):
    pass


def get_job_postings(session: Session) -> list[JobPosting]:
    stmt = select(JobPosting)
    return session.scalars(stmt).all()


def create_job_posting(session: Session, job_posting: JobPostingCreate) -> JobPosting:
    job = JobPosting(
        title=job_posting.title,
        company = job_posting.company,
        url = str(job_posting.url),
        location = job_posting.location,
        salary = job_posting.salary,
        note = job_posting.note,
        cover_letter_required = job_posting.cover_letter_required
    )

    try:
        session.add(job)
        session.commit()
        session.refresh(job)
        return job
    except IntegrityError as e:
        session.rollback()

        if "UNIQUE" in str(e.orig) and "job_postings.url" in str(e.orig) :
            raise DuplicateJobPostingError()
        raise




    