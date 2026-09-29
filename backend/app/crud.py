from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload, Session, selectinload
from datetime import datetime

from backend.app.models import JobPosting, Application, ApplicationMethod, ApplicationStatus
from .schemas import JobPostingCreate


class DuplicateJobPostingError(Exception):
    pass


class DuplicateApplicationError(Exception):
    pass


class JobPostingNotFoundError(Exception):
    pass


class ApplicationNotFoundError(Exception):
    pass


def get_job_postings(
    session: Session, 
    offset: int, 
    limit: int,
) -> tuple[list[JobPosting], int]:
    
    total_postings = session.scalar(select(func.count(JobPosting.id)))

    postings_stmt = (
        select(JobPosting)
        .order_by(JobPosting.saved_at.desc(), JobPosting.id.desc())
        .limit(limit)
        .offset(offset)
    )
    postings = session.scalars(postings_stmt).all()

    return postings, total_postings

def create_job_posting(session: Session, job_posting: JobPostingCreate) -> JobPosting:
    job = JobPosting(
        title=job_posting.title,
        company=job_posting.company,
        url=str(job_posting.url),
        location=job_posting.location,
        salary=job_posting.salary,
        note=job_posting.note,
        cover_letter_required=job_posting.cover_letter_required
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



# Applications

def create_application(
    session: Session,
    job_posting_id: int,
    how_applied: ApplicationMethod,
    *,
    applied_at: datetime | None = None
) -> Application:
    if applied_at is None:
        applied_at = datetime.now()
    application = Application(
        job_posting_id=job_posting_id,
        applied_at=applied_at,
        how_applied=how_applied,
    )

    try:
        session.add(application)
        session.commit()
        session.refresh(application)
        return application
    
    except IntegrityError as e:
        session.rollback()

        if "UNIQUE" in str(e.orig) and "applications.job_posting_id" in str(e.orig) :
            raise DuplicateApplicationError()

        if "FOREIGN KEY" in str(e.orig):
            raise JobPostingNotFoundError()
        
        raise



def get_job_applications(
    session: Session,
    offset: int,
    limit: int
) -> tuple[list[Application], int]:

    total = session.scalar(select(func.count(Application.id)))
    applications_stmt = (
        select(Application)
        .order_by(Application.applied_at.desc(), Application.id.desc())
        .limit(limit)
        .offset(offset)
        .options(selectinload(Application.job_posting))
    )
    applications = session.scalars(applications_stmt).all()

    return applications, total


def get_job_application(
    session: Session, 
    application_id: int
) -> Application:
    stmt = (
        select(Application)
        .where(Application.id == application_id)
        .options(joinedload(Application.job_posting))
    )
    application = session.execute(stmt).scalars().one_or_none()

    if not application:
        raise ApplicationNotFoundError

    return application

    