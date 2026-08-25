from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models import JobPosting


def get_job_postings(session: Session) -> list[JobPosting]:
    stmt = select(JobPosting)
    return session.scalars(stmt).all()