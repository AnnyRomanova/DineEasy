import pytest

from db.models import Table


@pytest.mark.asyncio
@pytest.mark.usefixtures("prepare_tables")
async def test_get_tables(async_client, tables: list[Table]):
    response = await async_client.get("/tables/")

    assert response.status_code == 200, response.text

    assert response.json() == [
        {
            "id": table.id,
            "name": table.name,
            "seats": table.seats,
            "location": table.location,
        }
        for table in tables
    ]
