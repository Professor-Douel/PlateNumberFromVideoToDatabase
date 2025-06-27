import datetime

from pydantic import BaseModel


class PlateNumber(BaseModel):
    number: str
    date_created: datetime.datetime
