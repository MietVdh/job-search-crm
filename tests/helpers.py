from datetime import datetime
import random
import uuid
from sqlalchemy.orm import Session
from backend.app.models import JobPosting

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