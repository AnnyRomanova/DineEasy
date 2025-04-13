import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app import app
from core.settings import Settings, get_settings
from db.connector import DatabaseConnector
from tables import table_controllers as table_module_controller
from reservations import reserve_controllers as reserve_module_controller

pytest_plugins = [
    "fixtures.test_db",
    "fixtures.prepare_table",
    "fixtures.prepare_tables",
    "fixtures.prepare_reservation",
    "fixtures.prepare_reservations",
]


@pytest.fixture(scope="session")
def settings() -> Settings:
    return get_settings()


@pytest.fixture(autouse=True)
def table_controller(
    dine_easy_db: DatabaseConnector,
) -> table_module_controller.TableController:
    table_module_controller.table_controller = table_module_controller.TableController(
        dine_easy_db
    )
    yield table_module_controller.table_controller


@pytest.fixture(autouse=True)
def reserve_controller(
    dine_easy_db: DatabaseConnector,
) -> reserve_module_controller.ReservationController:
    reserve_module_controller.reserve_controller = (
        reserve_module_controller.ReservationController(dine_easy_db)
    )
    yield reserve_module_controller.reserve_controller


@pytest_asyncio.fixture
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
