from app.core.config import settings
from app.services.base_service import BaseService
from fastapi import FastAPI
from app.api.v1.router import api_router

base = BaseService(settings, "rembg_services")
app = base.app

app.include_router(api_router, prefix=settings.API_V1_STR)
