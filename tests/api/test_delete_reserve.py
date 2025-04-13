from datetime import datetime, timedelta

import pytest
from db.connector import DatabaseConnector
from db.models import Reservation


@pytest.mark.asyncio
async def test_delete_reservation_204(
    async_client,
    dine_easy_db: DatabaseConnector,
    prepare_table: int,
):
    new_reservation_data = {
        "customer_name": "delete_test",
        "table_id": prepare_table,
        "reservation_time": (datetime.now() + timedelta(hours=2)).isoformat(),
        "duration_minutes": 45,
    }

    response_create = await async_client.post(
        "/reservations/", json=new_reservation_data
    )
    reservation_id = response_create.json()["id"]

    response_delete = await async_client.delete(f"/reservations/{reservation_id}")
    assert response_delete.status_code == 204
    assert response_delete.content == b""

    async with dine_easy_db.session_maker() as session:
        deleted = await session.get(Reservation, reservation_id)
        assert deleted is None


@pytest.mark.asyncio
async def test_delete_reservation_404(async_client):
    non_existent_id = 9999

    response = await async_client.delete(f"/reservations/{non_existent_id}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Бронь не найдена"}
