from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from app.core.mongodb import mongodb

logger = logging.getLogger(__name__)

class BaseService:
    def __init__(self, settings, service_name: str):
        @asynccontextmanager
        async def lifespan(app: FastAPI):
            await mongodb.connect_to_database()
            yield
            await mongodb.close_database_connection()

        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version=settings.VERSION,
            lifespan=lifespan,
            redirect_slashes=False
        )
        self.settings = settings
        self.service_name = service_name
        self._configure_middleware()

    def _configure_middleware(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

