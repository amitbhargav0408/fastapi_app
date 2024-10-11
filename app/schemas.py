from datetime import datetime
from pydantic import BaseModel

class ItemCreate(BaseModel):
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime

class ItemResponse(ItemCreate):
    id: str
    insert_date: datetime

class ClockInCreate(BaseModel):
    email: str
    location: str

class ClockInResponse(ClockInCreate):
    id: str
    insert_datetime: datetime
