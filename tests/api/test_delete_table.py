
import pytest

from db.connector import DatabaseConnector
from db.models import Table


@pytest.mark.asyncio
async def test_delete_table_204(async_client, dine_easy_db: DatabaseConnector, prepare_table):
    table_id = prepare_table
    response = await async_client.delete(f"/tables/{table_id}")
    assert response.status_code == 204, response.text
    assert response.content == b""

    async with dine_easy_db.session_maker() as session:
        deleted_table = await session.get(Table, table_id)
    assert deleted_table is None


@pytest.mark.asyncio
async def test_delete_table_404(async_client):
    response = await async_client.delete(f"/tables/10002")
    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Столик не найден"}