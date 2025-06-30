from sqlalchemy.orm import Session

from backend.db import models


def get_all_plate_numbers(db: Session):
    return db.query(models.DBPlateNumber).all()


def get_by_number(db: Session, plate_number: str):
    return db.query(models.DBPlateNumber).filter(
        models.DBPlateNumber.plate_number == plate_number
    ).first()
