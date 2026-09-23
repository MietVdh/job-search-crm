from fastapi.testclient import TestClient
from backend.app.main import app, get_session
from backend.app.schemas import JobPostingResponse
from .test_crud import engine, session
import pytest
from datetime import date


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



