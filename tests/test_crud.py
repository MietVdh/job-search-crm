import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from backend.app.crud import create_job_posting, get_job_postings, DuplicateJobPostingError, JobPostingNotFoundError
from backend.app.crud import get_job_applications, create_application, get_job_application, DuplicateApplicationError, ApplicationNotFoundError
from backend.app.schemas import JobPostingCreate, ApplicationCreate
from backend.app.models import Application, ApplicationMethod, ApplicationStatus
from tests.helpers import create_test_job_posting, create_test_job_posting_without_url, create_test_application


def test_database_starts_empty(session):
    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 0
    assert postings == []


def test_duplicate_job_posting_url_error(session):
    # Add first job posting to DB
    job_posting = JobPostingCreate(title="test developer", company="company inc.", url="http://www.example.com/666")
    create_job_posting(session, job_posting)


    # Try to add duplicate job posting
    with pytest.raises(DuplicateJobPostingError):
        duplicate_job_posting = JobPostingCreate(title="qa developer", company="some company", url="http://www.example.com/666")
        create_job_posting(session, duplicate_job_posting)

    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 1


def test_create_multiple_job_postings_with_no_url(session):
    create_test_job_posting_without_url(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting_without_url(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))

    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 2
    assert all(posting.url is None for posting in postings)


def test_get_job_postings_returns_requested_page_and_total(session):

    # Create three postings
    posting_a = create_test_job_posting(
        session,
        title="A",
        saved_at=datetime(2026, 1, 3, 12, 0, 0)
    )
    posting_b = create_test_job_posting(
        session,
        title="B",
        saved_at=datetime(2026, 1, 2, 12, 0, 0)
    )
    posting_c = create_test_job_posting(
        session,
        title="C",
        saved_at=datetime(2026, 1, 1, 12, 0, 0)
    )

    # Getting first page of results - page_size = 2
    postings, total = get_job_postings(
        session,
        offset=0,
        limit=2
    )

    assert total == 3
    assert [posting.title for posting in postings] == ["A", "B"]


def test_get_job_postings_returns_empty_list_for_page_beyond_end(session):
    # Create three postings
    create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    # Getting page 3 of results
    postings, total = get_job_postings(
        session,
        offset=4,
        limit=2
    )

    assert total == 3
    assert postings == []


def test_get_job_postings_orders_by_id_when_identical_saved_at(session):

    # Create 2 job postings with identical saved_at attributes
    create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 3, 12, 0, 0))

    postings, _ = get_job_postings(session, offset=0, limit=25)

    assert postings[0].saved_at == postings[1].saved_at
    assert postings[0].id > postings[1].id


def test_create_job_application(session):
    job_posting = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))

    job_application = create_test_application(session, job_posting.id)

    assert job_application.job_posting_id == job_posting.id
    assert job_application.status == ApplicationStatus.APPLIED
    assert job_application.job_posting is job_posting


def test_create_job_application_without_job_posting_error(session):
    job_application = Application(
        how_applied=ApplicationMethod.COMPANY_WEBSITE,
        status=ApplicationStatus.APPLIED,
    )

    session.add(job_application)

    with pytest.raises(IntegrityError):
        session.commit()



def test_create_job_application_with_nonexistend_job_posting_id_error(session):
    job_application = Application(
        job_posting_id=999999,
        how_applied=ApplicationMethod.COMPANY_WEBSITE,
        status=ApplicationStatus.APPLIED,
    )

    session.add(job_application)

    with pytest.raises(IntegrityError): # FOREIGN KEY constraint failed
        session.commit()



def test_multiple_applications_for_job_posting_error(session):
    job_posting = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    
    create_test_application(session, job_posting.id)

    with pytest.raises(IntegrityError): # UNIQUE constraint failed
        create_test_application(session, job_posting.id)


def test_delete_job_posting_with_application_error(session):
    job_posting = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
        
    create_test_application(session, job_posting.id)

    session.delete(job_posting)

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()


def test_delete_job_posting_without_application(session):
    job_posting = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))

    session.delete(job_posting)
    session.commit()

    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 0
    assert postings == []


def test_create_application(session):
    job_posting = create_test_job_posting(session, 'A')
    job_posting_id = job_posting.id

    before = datetime.now()


    application = ApplicationCreate(job_posting_id=job_posting_id, how_applied=ApplicationMethod.EMAIL)
    created = create_application(session, application)

    after = datetime.now()

    assert created.job_posting_id == job_posting_id
    assert created.how_applied == ApplicationMethod.EMAIL
    assert created.status == ApplicationStatus.APPLIED
    assert before <= created.applied_at <= after
    assert created.last_response_at is None


def test_create_application_with_applied_at(session):
    job_posting = create_test_job_posting(session, 'A')
    job_posting_id = job_posting.id
    applied_at = datetime(2026, 9, 25)

    application = ApplicationCreate(
        job_posting_id=job_posting_id, 
        how_applied=ApplicationMethod.EMAIL, 
        applied_at=applied_at)
    created = create_application(session, application)

    assert created.applied_at == applied_at


def test_create_application_missing_job_posting(session):

    with pytest.raises(JobPostingNotFoundError):
        application = ApplicationCreate(job_posting_id=9999, how_applied=ApplicationMethod.EMAIL)
        create_application(session, application)

    # Verify that session is still useable after error
    job_posting = create_test_job_posting(session, 'A')
    job_posting_id = job_posting.id

    application = ApplicationCreate(job_posting_id=job_posting_id, how_applied=ApplicationMethod.EMAIL)
    created = create_application(session, application)

    assert created.job_posting_id == job_posting_id
    

def test_create_duplicate_application(session):
    job_posting = create_test_job_posting(session, 'A')
    job_posting_id = job_posting.id

    application = ApplicationCreate(job_posting_id=job_posting_id, how_applied=ApplicationMethod.EMAIL)
    create_application(session, application)

    with pytest.raises(DuplicateApplicationError):
        create_application(session, application)

    assert get_job_applications(session, offset=0, limit=25)[1] == 1


def test_get_job_applications_returns_requested_page_and_total(session):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A")
    posting_b = create_test_job_posting(session, title="B")
    posting_c = create_test_job_posting(session, title="C")

    # Create applications for each job posting
    application_a = create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 4, 12, 0, 0))
    application_b = create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 6, 12, 0, 0))
    application_c = create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 5, 12, 0, 0))

    # Getting first page of results - page_size = 2
    applications, total = get_job_applications(
        session,
        offset=0,
        limit=2
    )

    assert total == 3
    assert applications == [application_b, application_c]
    assert [application.job_posting for application in applications] == [posting_b, posting_c]


def test_get_job_applications_orders_by_id_when_identical_applied_at(session):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A")
    posting_b = create_test_job_posting(session, title="B")
    posting_c = create_test_job_posting(session, title="C")

    # Create applications for each job posting
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 9, 6, 12, 0, 0))
    create_test_application(session, posting_b.id, applied_at=datetime(2026, 9, 6, 12, 0, 0))
    create_test_application(session, posting_c.id, applied_at=datetime(2026, 9, 5, 12, 0, 0))

    # Getting first page of results - page_size = 2
    applications, _ = get_job_applications(session, offset=0, limit=2)

    assert applications[0].applied_at == applications[1].applied_at
    assert applications[0].id > applications[1].id


def test_get_job_applications_respects_offset_and_limit(session):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A")
    posting_b = create_test_job_posting(session, title="B")
    posting_c = create_test_job_posting(session, title="C")

    # Create applications for each job posting
    application_a = create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 4, 12, 0, 0))
    application_b = create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 6, 12, 0, 0))
    application_c = create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 5, 12, 0, 0))

    # Getting first page of results - page_size = 2
    applications, total = get_job_applications(
        session,
        offset=1,
        limit=1
    )

    assert total == 3
    assert [application.job_posting for application in applications] == [posting_c]


def test_get_job_applications_database_starts_empty(session):
    applications, total = get_job_applications(session, offset=0, limit=25)
    assert total == 0
    assert applications == []


# Get a single application

def test_get_job_application_returns_existing_application(session):
    job_posting = create_test_job_posting(session, "A")
    application = create_test_application(session, job_posting.id, how_applied=ApplicationMethod.EMAIL)

    returned_application = get_job_application(session, application.id)

    assert returned_application.id == application.id
    assert returned_application.job_posting.title == "A"
    assert returned_application.how_applied == ApplicationMethod.EMAIL


def test_get_job_application_with_nonexistent_id_raises_error(session):
    with pytest.raises(ApplicationNotFoundError):
        get_job_application(session, 9999)