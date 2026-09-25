import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from backend.app.database import Base



@pytest.fixture
def engine():
    engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)
    return engine
    

@pytest.fixture
def session(engine):
    SessionFactory = sessionmaker(engine)
    session = SessionFactory()
    yield session
    session.close()