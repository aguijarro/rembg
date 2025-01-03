from motor.motor_asyncio import AsyncIOMotorClient
import os

class MongoDB:
    def __init__(self):
        self.client = None
        self.db = None

    async def connect_to_database(self, path: str = None):
        # Use environment variable if provided, otherwise use default
        mongodb_url = path or os.getenv("MONGODB_URL", "mongodb://localhost:27017")
        try:
            self.client = AsyncIOMotorClient(mongodb_url, serverSelectionTimeoutMS=5000)
            # Use test_database as defined in the original code
            self.db = self.client.test_database
            # Verify connection
            await self.client.admin.command('ping')
            print(f"Successfully connected to MongoDB at {mongodb_url}")
        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")
            raise e

    async def close_database_connection(self):
        if self.client:
            self.client.close()

mongodb = MongoDB()
