
from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

from .database import SessionLocal  # Import the plumbing we just built

app = FastAPI()


# Dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    # Simple check to see if the DB is alive
    try:
        db.execute(text("SELECT 1"))
        db_status = "Connected"
    except Exception as e:
        db_status = f"Disconnected: {e}"

    return {
        "Status": "Look Ma, no hands!",
        "Version": "2.0-Automatic",
        "Database": db_status,
    }
