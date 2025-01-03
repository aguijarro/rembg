from datetime import datetime
from app.core.mongodb import mongodb

class HealthRepository:
    @staticmethod
    async def create_item(name: str):
        test_item = {
            "name": name,
            "created_at": datetime.utcnow()
        }
        result = await mongodb.db.test_collection.insert_one(test_item)
        test_item["_id"] = str(result.inserted_id)
        return test_item

    @staticmethod
    async def get_all_items():
        cursor = mongodb.db.test_collection.find({})
        items = []
        async for document in cursor:
            document["id"] = str(document.pop("_id"))
            items.append(document)
        return items
