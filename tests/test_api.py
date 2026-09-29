import pytest
from datetime import date, datetime
from fastapi.testclient import TestClient
from backend.app.main import app, get_session
from backend.app.models import ApplicationMethod, ApplicationStatus
from backend.app.schemas import JobPostingResponse
from tests.helpers import create_test_job_posting, create_test_application


client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, Career CRM!"}



@pytest.fixture
def test_session_override(session):
    def get_test_session():
        yield session

    app.dependency_overrides[get_session] = get_test_session

    yield

    app.dependency_overrides = {}
    

def test_create_job_posting(test_session_override):
    payload = {
        "title": "Software Developer",
        "company": "Dotcom Inc",
        "url": "http://www.example.com/777"
    }

    response = client.post("/job-postings", json=payload)
    assert response.status_code == 201
    data = response.json()

    assert data["title"] == "Software Developer"
    assert data["company"] == "Dotcom Inc"
    assert data["url"] == "http://www.example.com/777"
    assert "saved_at" in data
    assert data["id"] > 0
    assert data["location"] is None
    assert data["salary"] is None
    assert data["note"] is None
    assert data["cover_letter_required"] is False


def test_create_duplicate_job_posting(test_session_override):
    original_payload = {
        "title": "Software Developer",
        "company": "Dotcom Inc",
        "url": "http://www.example.com/777"
    }

    original_response = client.post("/job-postings", json=original_payload)
    assert original_response.status_code == 201

    duplicate_payload = {
        "title": "QA Tester",
        "company": "ABC Corporation",
        "url": "http://www.example.com/777"
    }
    
    duplicate_response = client.post("/job-postings", json=duplicate_payload)
    assert duplicate_response.status_code == 409
    data = duplicate_response.json()
    assert data == {
        "detail": "A job posting with that URL already exists."
    }


def test_get_job_postings_returns_requested_page_and_total(session, test_session_override):
    # Create three postings
    create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    response = client.get("/job-postings?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert len(data) == 4
    
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert [posting["title"] for posting in data["items"]] == ["A", "B"]


def test_get_job_postings_uses_default_pagination_parameters(session, test_session_override):
    # Create two postings
    create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    
    response = client.get("/job-postings")
    assert response.status_code == 200
    data = response.json()
    
    assert data["page"] == 1
    assert data["page_size"] == 25
    assert data["total"] == 2
    assert [posting["title"] for posting in data["items"]] == ["A", "B"]


@pytest.mark.parametrize(
    "query_string",
    [
        pytest.param("?page=0", id="page-zero"),
        pytest.param("?page_size=0", id="page-size-zero"),
        pytest.param("?page_size=51", id="page-size-too-large"),
    ],
)
def test_get_job_postings_rejects_invalid_pagination_parameters(query_string):
    
    response = client.get(f"/job-postings{query_string}")
    assert response.status_code == 422


def test_get_job_postings_returns_empty_page_when_page_is_beyond_end(session, test_session_override):
    # Create three postings
    create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    response = client.get("/job-postings?page=3&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 3
    assert data["items"] == []


# /applications
def test_get_applications_returns_empty_page_when_database_is_empty(session, test_session_override):
    response = client.get("/applications")
    assert response.status_code == 200
    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 25
    assert data["total"] == 0
    assert data["items"] == []


def test_get_applications_returns_requested_page_and_total(session, test_session_override):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    posting_b = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    posting_c = create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    # Create three applications
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 10, 14, 15))
    create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 10, 14, 25))
    create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 10, 14, 20))

    response = client.get("/applications?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert [application["job_title"] for application in data["items"]] == ["B", "C"]


def test_get_applications_serializes_application_list_item(session, test_session_override):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    posting_b = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    posting_c = create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    # Create three applications
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 10, 14, 15))
    application_b = create_test_application(
        session, 
        posting_b.id, 
        applied_at=datetime(2026, 1, 10, 14, 25), 
        how_applied=ApplicationMethod.EMAIL,
        status=ApplicationStatus.INVITED_TO_TEST,
        last_response_at=datetime(2026, 2, 3, 12, 0)
    )
    create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 10, 14, 20))

    response = client.get("/applications?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()

    first_returned_application = data["items"][0]
    second_returned_application = data["items"][1]
    assert first_returned_application["job_title"] == "B"
    assert first_returned_application["company"] == "Test Company"
    assert first_returned_application["applied_at"] == "2026-01-10"
    assert first_returned_application["how_applied"] == "email"
    assert first_returned_application["last_response_at"] == "2026-02-03"
    assert first_returned_application["status"] == "invited_to_test"
    assert first_returned_application["job_posting_id"] == posting_b.id
    assert first_returned_application["id"] == application_b.id

    assert second_returned_application["last_response_at"] is None
    assert second_returned_application["job_title"] == "C"


def test_get_applications_orders_applications_by_application_date_and_id(session, test_session_override):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    posting_b = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    posting_c = create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    # Create three applications
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 10, 14, 25))
    create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 10, 14, 25))
    create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 10, 14, 20))

    response = client.get("/applications?page=1&page_size=2")
    assert response.status_code == 200
    data = response.json()

    # A and B have the same applied_at; B has the higher id
    assert [application["job_title"] for application in data["items"]] == ["B", "A"]


def test_get_applications_uses_default_pagination_parameters(session, test_session_override):
    # Create two postings
    posting_a = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    posting_b = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
 
    # Create two applications
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 10, 14, 20))
    create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 10, 14, 25))
    
    response = client.get("/applications")
    assert response.status_code == 200
    data = response.json()
    
    assert data["page"] == 1
    assert data["page_size"] == 25
    assert data["total"] == 2


@pytest.mark.parametrize(
    "query_string",
    [
        pytest.param("?page=0", id="page-zero"),
        pytest.param("?page_size=0", id="page-size-zero"),
        pytest.param("?page_size=51", id="page-size-too-large"),
    ],
)
def test_get_applications_rejects_invalid_pagination_parameters(query_string):
    
    response = client.get(f"/applications{query_string}")
    assert response.status_code == 422


def test_get_applications_returns_empty_page_when_page_is_beyond_end(session, test_session_override):
    # Create three postings
    posting_a = create_test_job_posting(session, title="A", saved_at=datetime(2026, 1, 3, 12, 0, 0))
    posting_b = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    posting_c = create_test_job_posting(session, title="C", saved_at=datetime(2026, 1, 1, 12, 0, 0))

    # Create three applications
    create_test_application(session, posting_a.id, applied_at=datetime(2026, 1, 10, 14, 20))
    create_test_application(session, posting_b.id, applied_at=datetime(2026, 1, 10, 14, 25))
    create_test_application(session, posting_c.id, applied_at=datetime(2026, 1, 10, 14, 15))

    response = client.get("/applications?page=3&page_size=2")
    assert response.status_code == 200
    data = response.json()

    assert data["total"] == 3
    assert data["items"] == []


def test_get_single_application_returns_correct_fields(session, test_session_override):
    posting = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    application = create_test_application(
        session, 
        posting.id, 
        applied_at=datetime(2026, 1, 10, 14, 25), 
        how_applied=ApplicationMethod.EMAIL,
        status=ApplicationStatus.INVITED_TO_TEST,
        last_response_at=datetime(2026, 2, 3, 12, 0)
    )

    response = client.get(f"/applications/{application.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "B"
    assert data["company"] == "Test Company"
    assert data["applied_at"] == "2026-01-10"
    assert data["how_applied"] == "email"
    assert data["last_response_at"] == "2026-02-03"
    assert data["status"] == "invited_to_test"
    assert data["job_posting_id"] == posting.id
    assert data["id"] == application.id
    assert data["note"] is None


def test_get_single_application_with_nonexistent_id_returns_404_error(session, test_session_override):
    response = client.get("/applications/9999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Application not found"


def test_get_single_application_with_invalid_path_parameter_returns_422_error(session, test_session_override):
    response = client.get("/applications/foo")
    
    assert response.status_code == 422


def test_create_application_returns_application_detail(session, test_session_override):
    posting = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    payload = {
        "job_posting_id": posting.id,
        "how_applied": "email"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["how_applied"] == "email"
    assert data["status"] == "applied"
    assert data["job_title"] == "B"
    assert data["saved_at"] == "2026-01-02"
    assert data["location"] is None
    assert data["salary"] is None
    assert data["note"] is None
    assert data["cover_letter_required"] is False
    assert data["last_response_at"] is None
    assert data["applied_at"] == str(date.today())


def test_create_application_with_historical_applied_at_returns_application_detail(session, test_session_override):
    posting = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    payload = {
        "job_posting_id": posting.id,
        "how_applied": "email",
        "applied_at": "2026-01-10"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["applied_at"] == "2026-01-10"


def test_create_duplicate_application_returns_409_error(session, test_session_override):
    posting = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    payload = {
        "job_posting_id": posting.id,
        "how_applied": "email"
    }
    first_response = client.post("/applications", json=payload)
    assert first_response.status_code == 201

    response = client.post("/applications", json=payload)

    assert response.status_code == 409
    assert response.json()["detail"] == "An application associated with that job posting already exists"


def test_create_application_for_nonexistent_job_posting_returns_404_error(session, test_session_override):
    payload = {
        "job_posting_id": 9999,
        "how_applied": "email"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Job posting not found"


def test_create_application_with_invalid_request_body_returns_422_error(session, test_session_override):
    posting = create_test_job_posting(session, title="B", saved_at=datetime(2026, 1, 2, 12, 0, 0))
    payload = {
        "job_posting_id": posting.id,
        "foo": "bar"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 422

    payload = {
        "job_posting_id": posting.id,
        "how_applied": "carrier_pigeon"
    }

    response = client.post("/applications", json=payload)
    assert response.status_code == 422