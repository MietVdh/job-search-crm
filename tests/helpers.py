from datetime import datetime
import random
import uuid
from sqlalchemy.orm import Session
from backend.app.models import JobPosting, Application, ApplicationStatus, ApplicationMethod

def create_test_job_posting(
    session: Session, 
    title: str,
    saved_at: datetime | None = None
) -> JobPosting:
    
    job = JobPosting(
        title=title,
        company="Test Company",
        url=f"http://www.example.com/{uuid.uuid4()}",
        saved_at=saved_at if saved_at is not None else datetime.now()
    )

    session.add(job)
    session.flush()
    return job


def create_test_job_posting_without_url(
    session: Session, 
    title: str,
    saved_at: datetime | None = None
) -> JobPosting:
    
    job = JobPosting(
        title=title,
        company="Test Company",
        saved_at=saved_at if saved_at is not None else datetime.now()
    )

    session.add(job)
    session.flush()
    return job


def create_test_application(
        session: Session,
        job_posting_id: int,
        applied_at: datetime | None = None,
        how_applied: ApplicationMethod = ApplicationMethod.COMPANY_WEBSITE,
        status: ApplicationStatus = ApplicationStatus.APPLIED,
        last_response_at: datetime | None = None
) -> Application:
    application = Application(
        job_posting_id=job_posting_id,
        applied_at=applied_at,
        how_applied=how_applied,
        status=status,
        last_response_at=last_response_at
    )

    session.add(application)
    session.flush()
    return application