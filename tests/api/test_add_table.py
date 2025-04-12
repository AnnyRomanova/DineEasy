from unittest.mock import ANY

import pytest

from db.connector import DatabaseConnector
from db.models import Table


@pytest.mark.asyncio
async def test_create_table_and_duplicate(async_client, dine_easy_db: DatabaseConnector):
    new_table_data = {"name": "test_name", "seats": 2, "location": "test_location"}

    response = await async_client.post("/tables/", json=new_table_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data == {
        "id": ANY,
        "name": "test_name",
        "seats": 2,
        "location": "test_location"
    }

    async with dine_easy_db.session_maker() as session:
        dine_easy_db = await session.get(Table, data["id"])
    assert dine_easy_db.name == data["name"]
    assert dine_easy_db.location == data["location"]

    duplicate_response = await async_client.post("/tables/", json=new_table_data)
    assert duplicate_response.status_code == 400, duplicate_response.text
    assert duplicate_response.json() == {
        "detail": f'Столик с именем "{new_table_data['name']}" уже существует'
    }
