import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from backend.app.main import app, get_session
from backend.app.schemas import JobPostingResponse
from tests.helpers import create_test_job_posting


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
    