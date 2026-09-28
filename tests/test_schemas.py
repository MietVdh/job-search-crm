import pytest
from datetime import date, datetime

from tests.helpers import create_test_job_posting, create_test_application
from backend.app.models import ApplicationMethod
from backend.app.schemas import ApplicationListItem, ApplicationDetail



def test_application_list_item_from_orm_application(session):
    job_posting = create_test_job_posting(session, "Backend Developer")
    job_posting_id = job_posting.id

    application = create_test_application(
        session, 
        job_posting_id, 
        applied_at=datetime(2026, 9, 20, 14, 30), 
        how_applied=ApplicationMethod.COMPANY_WEBSITE
    )
    application.last_response_at = datetime(2026, 9, 25, 9, 15)

    result = ApplicationListItem.model_validate(application)

    data = result.model_dump(mode="json")
    assert data["status"] == "applied"
    assert data["applied_at"] == str(date(2026, 9, 20))
    assert data["last_response_at"] == str(date(2026, 9, 25))
    
    assert result.job_title == "Backend Developer"
    assert result.company == "Test Company"

    
def test_application_detail_from_orm_application(session):
    job_posting = create_test_job_posting(session, "Backend Developer", saved_at=(datetime(2026, 8, 30, 12, 30)))
    job_posting_id = job_posting.id
    job_posting.location = "Montreal"
    job_posting.salary = "$75,000 - $90,000"
    job_posting.note = "Interesting role - unlimited PTO!"
    job_posting.cover_letter_required = True

    application = create_test_application(
        session, 
        job_posting_id, 
        applied_at=datetime(2026, 9, 20, 14, 30), 
        how_applied=ApplicationMethod.COMPANY_WEBSITE
    )
    application.last_response_at = datetime(2026, 9, 25, 9, 15)

    result = ApplicationDetail.model_validate(application)

    data = result.model_dump(mode="json")
    assert data["status"] == "applied"
    assert data["how_applied"] == "company_website"
    assert data["saved_at"] == str(date(2026, 8, 30))
    assert data["applied_at"] == str(date(2026, 9, 20))
    assert data["last_response_at"] == str(date(2026, 9, 25))
    
    assert result.job_title == "Backend Developer"
    assert result.company == "Test Company"
    assert result.note == "Interesting role - unlimited PTO!"
    assert result.cover_letter_required is True
    assert result.location == "Montreal"
    assert result.salary == "$75,000 - $90,000"
