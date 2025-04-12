from datetime import datetime, timedelta
import random

import pytest
import pytest_asyncio

from db.connector import DatabaseConnector
from db.models import Reservation


@pytest.fixture
def reservations(tables: list) -> list[Reservation]:
    base_date = datetime(2025, 12, 1, 12, 0)
    reservations = []

    for i in range(5):
        random_days = random.randint(0, 30)
        random_minutes = random.randint(0, 720)
        reservation_time = base_date + timedelta(days=random_days, minutes=random_minutes)

        reservations.append(
            Reservation(
                customer_name=f"test_customer_name_{i}",
                table_id=tables[i].id if i < len(tables) else tables[0].id,
                reservation_time=reservation_time,
                duration_minutes=random.choice([30, 60, 90])
            )
        )

    return reservations

@pytest_asyncio.fixture
async def prepare_reservations(dine_easy_db: DatabaseConnector, prepare_tables, reservations: list[Reservation]) -> list[Reservation]:
    async with dine_easy_db.session_maker(expire_on_commit=False) as session:
        session.add_all(reservations)
        await session.commit()
        return reservations