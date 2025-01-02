from fastapi import APIRouter
from app.core.mongodb import mongodb
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.post("/health_db")
async def create_test(name: str):
    test_item = {
        "name": name,
        "created_at": datetime.utcnow()
    }
    result = await mongodb.db.test_collection.insert_one(test_item)
    test_item["_id"] = str(result.inserted_id)
    return test_item

@router.get("/health_db")
async def read_tests():
    cursor = mongodb.db.test_collection.find({})
    tests = []
    async for document in cursor:
        document["_id"] = str(document["_id"])
        tests.append(document)
    return tests       
