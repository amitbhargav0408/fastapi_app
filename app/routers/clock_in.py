from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.database import clock_in_collection
from app.schemas import ClockInCreate, ClockInResponse

router = APIRouter()

@router.post("/clock-in", response_model=ClockInResponse)
async def create_clock_in(clock_in: ClockInCreate):
    insert_datetime = datetime.now()
    clock_in_dict = clock_in.dict()
    clock_in_dict["insert_datetime"] = insert_datetime
    result = clock_in_collection.insert_one(clock_in_dict)
    return {**clock_in_dict, "id": str(result.inserted_id), "insert_datetime": insert_datetime}

@router.get("/clock-in/{record_id}", response_model=ClockInResponse)
async def get_clock_in(record_id: str):
    record = clock_in_collection.find_one({"_id": ObjectId(record_id)})
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {**record, "id": str(record["_id"])}

@router.get("/clock-in/filter")
async def filter_clock_ins(email: str = None, location: str = None, insert_datetime: datetime = None):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        query["insert_datetime"] = {"$gt": insert_datetime}
    
    records = list(clock_in_collection.find(query))
    return [{"id": str(record["_id"]), **record} for record in records]

@router.delete("/clock-in/{record_id}")
async def delete_clock_in(record_id: str):
    result = clock_in_collection.delete_one({"_id": ObjectId(record_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"detail": "Record deleted"}

@router.put("/clock-in/{record_id}", response_model=ClockInResponse)
async def update_clock_in(record_id: str, clock_in: ClockInCreate):
    update_data = clock_in.dict()
    result = clock_in_collection.update_one({"_id": ObjectId(record_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Record not found or no changes made")
    updated_record = clock_in_collection.find_one({"_id": ObjectId(record_id)})
    return {**updated_record, "id": str(updated_record["_id"])}
