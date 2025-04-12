import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Table


@pytest.fixture
def tables() -> list[Table]:
    return [
        Table(
            name=f"test_name_{i}",
            seats=i,
            location=f"test_location_{i}"
        )
        for i in range(1, 11)
    ]

@pytest_asyncio.fixture
async def prepare_tables(dine_easy_db: DatabaseConnector, tables: list[Table]) -> None:
    async with dine_easy_db.session_maker(expire_on_commit=False) as session:
        session.add_all(tables)
        await session.commit()