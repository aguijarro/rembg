from fastapi import APIRouter
from app.repositories.health_repository import HealthRepository

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/health_db")
async def create_db_row(name: str):
    return await HealthRepository.create_item(name)

@router.get("/health_db")
async def read_db_rows():
    return await HealthRepository.get_all_items()       
