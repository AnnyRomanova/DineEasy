import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

import controllers.controllers as module_controllers
from api.routers import router
from core.settings import get_settings
from db.connector import DatabaseConnector

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Actions before launching the application")
    db_connector = DatabaseConnector(settings.DB.asyncpg_url)
    module_controllers.table_controller = module_controllers.TableController(db_connector)
    module_controllers.reserve_controller = module_controllers.ReservationController(db_connector)
    yield
    await db_connector.disconnect()
    logger.info("Actions after launching the application")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_config="core/logging.yaml")