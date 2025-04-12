import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app import app
from core.settings import Settings, get_settings
from db.connector import DatabaseConnector
import controllers.controllers as module_controllers

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_table",
    "fixtures.prepare_tables",
    "fixtures.prepare_reservation",
    "fixtures.prepare_reservations"
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(autouse=True)
def table_controller(dine_easy_db: DatabaseConnector) -> module_controllers.TableController:
    module_controllers.table_controller = module_controllers.TableController(dine_easy_db)
    yield module_controllers.table_controller


@pytest.fixture(autouse=True)
def reserve_controller(dine_easy_db: DatabaseConnector) -> module_controllers.ReservationController:
    module_controllers.reserve_controller = module_controllers.ReservationController(dine_easy_db)
    yield module_controllers.reserve_controller


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client