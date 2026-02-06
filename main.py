from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import models  # <--- Import your new file
from database import Base, SessionLocal, engine

# This line tells SQLAlchemy to create the tables in your DB if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root(db: Session = Depends(get_db)):
    return {"Status": "Live", "Database": "Connected"}


@app.post("/items/")
def create_item(title: str, description: str, db: Session = Depends(get_db)):
    new_item = models.Item(title=title, description=description)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@app.get("/items/")
def read_items(db: Session = Depends(get_db)):
    # This queries the 'items' table and returns every row it finds
    items = db.query(models.Item).all()
    return items
