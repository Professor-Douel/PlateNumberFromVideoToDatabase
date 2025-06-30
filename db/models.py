import datetime

from sqlalchemy import Column, Integer, String, DateTime

from backend.db.engine import Base


class DBPlateNumber(Base):
    __tablename__ = 'plate_number'

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String(20), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.utcnow)
