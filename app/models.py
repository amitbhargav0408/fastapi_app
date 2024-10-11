from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    email: str
    item_name: str
    quantity: int
    expiry_date: datetime

class ClockInRecord(BaseModel):
    email: str
    location: str
