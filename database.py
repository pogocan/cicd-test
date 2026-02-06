import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Grab the URL from the environment (Render or GitHub)
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Setup for SQLite vs. Postgres compatibility
if DATABASE_URL and DATABASE_URL.startswith("sqlite"):
    # SQLite needs this specific 'check_same_thread' fix for FastAPI
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Use standard settings for PostgreSQL
    engine = create_engine(DATABASE_URL)

# 3. Create the Session and Base classes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
