import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Table


@pytest.fixture
def table() -> Table:
    return Table(name="test_name", seats=6, location="test_location")


@pytest_asyncio.fixture
async def prepare_table(dine_easy_db: DatabaseConnector, table: Table) -> int:
    async with dine_easy_db.session_maker(expire_on_commit=False) as session:
        session.add(table)
        await session.commit()
        return table.id
