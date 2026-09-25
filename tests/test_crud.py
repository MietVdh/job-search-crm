import pytest
from datetime import datetime
from backend.app.crud import create_job_posting, get_job_postings, DuplicateJobPostingError
from backend.app.schemas import JobPostingCreate
from tests.helpers import create_test_job_posting


def test_database_starts_empty(session):
    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 0
    assert postings == []


def test_duplicate_job_posting_error(session):
    # Add first job posting to DB
    job_posting = JobPostingCreate(title="test developer", company="company inc.", url="http://www.example.com/666")
    create_job_posting(session, job_posting)


    # Try to add duplicate job posting
    with pytest.raises(DuplicateJobPostingError):
        duplicate_job_posting = JobPostingCreate(title="qa developer", company="some company", url="http://www.example.com/666")
        create_job_posting(session, duplicate_job_posting)

    postings, total = get_job_postings(session, offset=0, limit=25)
    assert total == 1


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