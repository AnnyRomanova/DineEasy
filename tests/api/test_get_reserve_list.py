from datetime import timezone

import pytest

from db.models import Reservation


@pytest.mark.asyncio
async def test_get_reservations(
    async_client, prepare_tables, prepare_reservations, reservations: list[Reservation]
):
    response = await async_client.get("/reservations/")

    assert response.status_code == 200, response.text

    assert response.json() == [
        {
            "id": reservation.id,
            "customer_name": reservation.customer_name,
            "table_id": reservation.table_id,
            "reservation_time": reservation.reservation_time.astimezone(timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z"),
            "duration_minutes": reservation.duration_minutes,
        }
        for reservation in reservations
    ]
