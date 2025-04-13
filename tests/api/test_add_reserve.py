from datetime import datetime, timedelta, timezone

import pytest


@pytest.mark.asyncio
async def test_create_reservation_and_duplicate(async_client, prepare_table: int):
    reservation_time = (datetime.now(timezone.utc) + timedelta(hours=1)).replace(
        microsecond=0
    )

    new_reservation_data = {
        "customer_name": "test_name",
        "table_id": prepare_table,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 60,
    }

    response_1 = await async_client.post("/reservations/", json=new_reservation_data)
    assert response_1.status_code == 201
    data = response_1.json()
    assert data["table_id"] == prepare_table

    response_2 = await async_client.post("/reservations/", json=new_reservation_data)
    assert response_2.status_code == 400
    assert response_2.json() == {"detail": "Столик на это время уже забронирован"}


@pytest.mark.asyncio
async def test_create_reservation_in_the_past(async_client, prepare_table: int):
    reservation_time = (datetime.now(timezone.utc) - timedelta(hours=2)).replace(
        microsecond=0
    )

    new_reservation_data = {
        "customer_name": "past_client",
        "table_id": prepare_table,
        "reservation_time": reservation_time.isoformat(),
        "duration_minutes": 30,
    }

    response = await async_client.post("/reservations/", json=new_reservation_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Нельзя забронировать столик в прошлом"}
