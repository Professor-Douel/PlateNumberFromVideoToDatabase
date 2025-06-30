from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from db.engine import SessionLocal
import crud

app = FastAPI()


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/plates/")
def plates(db: Session = Depends(get_db)):
    return crud.get_all_plate_numbers(db)

@app.get("/plates/{plate_number}/")
def plate(plate_number: str, db: Session = Depends(get_db)):
    db_plate_number = crud.get_by_number(db=db, plate_number=plate_number)

    if db_plate_number is None:
        raise HTTPException(
            status_code=404,
            detail="Number not found",
        )
    return db_plate_number
