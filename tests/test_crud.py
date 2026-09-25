import pytest
from backend.app.crud import create_job_posting, get_job_postings, DuplicateJobPostingError
from backend.app.schemas import JobPostingCreate


def test_database_starts_empty(session):
    assert len(get_job_postings(session, 0, 10)[0]) == 0


def test_duplicate_job_posting_error(session):
    # Add first job posting to DB
    job_posting = JobPostingCreate(title="test developer", company="company inc.", url="http://www.example.com/666")
    create_job_posting(session, job_posting)


    # Try to add duplicate job posting
    with pytest.raises(DuplicateJobPostingError):
        duplicate_job_posting = JobPostingCreate(title="qa developer", company="some company", url="http://www.example.com/666")
        create_job_posting(session, duplicate_job_posting)
    assert len(get_job_postings(session, 0, 10)[0]) == 1


