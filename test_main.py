import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .database import DATABASE_URL, Base
from .main import app, get_db

# Create a dedicated engine for testing
# Note: SQLite in tests is fast and isolated
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the database tables in our test SQLite file
Base.metadata.create_all(bind=engine)


# This replaces the real 'get_db' with our testing version
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    # Update this to match your new JSON structure
    assert response.json() == {
        "Status": "Look Ma, no hands!",
        "Version": "2.0-Automatic",
        "Database": "Connected",
    }
