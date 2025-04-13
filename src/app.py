import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from tables import table_controllers as table_module_controller
from reservations import reserve_controllers as reserve_module_controller

from tables.table_api import router as table_router
from reservations.reserve_api import router as reserve_router
from core.settings import get_settings
from db.connector import DatabaseConnector

logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    logger.info("Actions before launching the application")
    db_connector = DatabaseConnector(settings.DB.asyncpg_url)
    table_module_controller.table_controller = table_module_controller.TableController(
        db_connector
    )
    reserve_module_controller.reserve_controller = (
        reserve_module_controller.ReservationController(db_connector)
    )
    yield
    await db_connector.disconnect()
    logger.info("Actions after launching the application")


app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

app.include_router(table_router)
app.include_router(reserve_router)


if __name__ == "__main__":
    uvicorn.run("app:app", port=8000, log_config="core/logging.yaml")
