from fastapi import APIRouter, HTTPException
from datetime import datetime
from bson import ObjectId
from app.database import items_collection
from app.schemas import ItemCreate, ItemResponse

router = APIRouter()

@router.post("/items", response_model=ItemResponse)
async def create_item(item: ItemCreate):
    insert_date = datetime.now()
    item_dict = item.dict()
    item_dict["insert_date"] = insert_date
    result = items_collection.insert_one(item_dict)
    return {**item_dict, "id": str(result.inserted_id), "insert_date": insert_date}

@router.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    item = items_collection.find_one({"_id": ObjectId(item_id)})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {**item, "id": str(item["_id"])}

@router.get("/items/filter")
async def filter_items(email: str = None, expiry_date: datetime = None, insert_date: datetime = None, quantity: int = None):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        query["expiry_date"] = {"$gt": expiry_date}
    if insert_date:
        query["insert_date"] = {"$gt": insert_date}
    if quantity is not None:
        query["quantity"] = {"$gte": quantity}
    
    items = list(items_collection.find(query))
    return [{"id": str(item["_id"]), **item} for item in items]

@router.get("/items/aggregate")
async def aggregate_items():
    pipeline = [
        {"$group": {"_id": "$email", "count": {"$sum": 1}}}
    ]
    result = list(items_collection.aggregate(pipeline))
    return result

@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    result = items_collection.delete_one({"_id": ObjectId(item_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"detail": "Item deleted"}

@router.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate):
    update_data = item.dict()
    result = items_collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Item not found or no changes made")
    updated_item = items_collection.find_one({"_id": ObjectId(item_id)})
    return {**updated_item, "id": str(updated_item["_id"])}
