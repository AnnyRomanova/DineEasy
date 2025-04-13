from datetime import datetime, timezone

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Reservation


@pytest.fixture
def reservation() -> Reservation:
    return Reservation(
        customer_name="test_customer_name",
        table_id=1,
        reservation_time=datetime(2025, 12, 31, 23, 59, 59, tzinfo=timezone.utc),
        duration_minutes=60,
    )


@pytest_asyncio.fixture
async def prepare_reservation(
    dine_easy_db: DatabaseConnector, reservation: Reservation, prepare_table
) -> Reservation:
    async with dine_easy_db.session_maker(expire_on_commit=False) as session:
        session.add(reservation)
        await session.commit()
        await session.refresh(reservation)
        return reservation
