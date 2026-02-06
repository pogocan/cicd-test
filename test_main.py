from database import DATABASE_URL, Base
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, get_db

# 1. Setup the Test Database (SQLite)
# DATABASE_URL is 'sqlite:///./test.db' inside GitHub Actions
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Create the tables in the test database
Base.metadata.create_all(bind=engine)


# 3. Define the Dependency Override
# This swaps the real 'get_db' for this test version automatically
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


# 4. The Tests
def test_read_main():
    """Verify the root endpoint and database connection."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Status": "Live", "Database": "Connected"}


def test_create_item():
    """Verify we can actually save data to the database."""
    response = client.post(
        "/items/",
        params={"title": "CI Test Item", "description": "Testing our pipeline"},
    )
    assert response.status_code == 200
