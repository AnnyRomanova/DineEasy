import logging
from datetime import timedelta, datetime

from fastapi import HTTPException

from sqlalchemy import select

from db.connector import DatabaseConnector

import schemas.model as pydentic_models
import db.models as db_models

logger = logging.getLogger(__name__)


class TableController:

    def __init__(self, db: DatabaseConnector) -> None:
        self.db = db

    async def get_tables_list(self) -> list[pydentic_models.TableOUT]:
        logger.info("Table list requested")
        async with self.db.session_maker() as session:
            request = select(db_models.Table).order_by(db_models.Table.id)
            cursor = await session.execute(request)
            tables = cursor.scalars().all()
            tables_list = []
            for table in tables:
                tables_list.append(pydentic_models.TableOUT(
                    id=table.id,
                    name=table.name,
                    seats=table.seats,
                    location=table.location
                ))
            return tables_list

    async def add_table(self, table_data: pydentic_models.TableCreate) -> pydentic_models.TableOUT:
        logger.info("Request to add new table")
        async with self.db.session_maker() as session:
            table_name_request = select(db_models.Table).where(db_models.Table.name == table_data.name)
            result = await session.execute(table_name_request)
            table_name = result.scalar_one_or_none()

            if table_name:
                logger.error(f"Table with name {table_data.name} already exists")
                raise HTTPException(status_code=400, detail=f'Столик с именем "{table_data.name}" уже существует')

            new_table = db_models.Table(**table_data.model_dump())
            session.add(new_table)
            await session.commit()

            await session.refresh(new_table)

            return pydentic_models.TableOUT.model_validate(new_table)

    async def delete_table(self, table_id: int) -> None:
        logger.info("Request to delete the table")
        async with self.db.session_maker() as session:
            delete_request = select(db_models.Table).where(db_models.Table.id == table_id)
            cursor = await session.execute(delete_request)
            existing_table = cursor.scalar_one_or_none()

            if not existing_table:
                raise HTTPException(status_code=404, detail="Столик не найден")

            delete_reservations_request = select(db_models.Reservation).where(
                db_models.Reservation.table_id == table_id
            )
            reservations_result = await session.execute(delete_reservations_request)
            reservations = reservations_result.scalars().all()

            for reservation in reservations:
                await session.delete(reservation)

            await session.delete(existing_table)
            await session.commit()
        logger.info("Table deleted")


class ReservationController:

    def __init__(self, db: DatabaseConnector) -> None:
        self.db = db

    async def get_reserve_list(self) -> list[pydentic_models.ReserveOUT]:
        logger.info("Reservations list requested")
        async with self.db.session_maker() as session:
            request = select(db_models.Reservation).order_by(db_models.Reservation.id)
            cursor = await session.execute(request)
            reservations = cursor.scalars().all()
            reservations_list = []
            for reservation in reservations:
                reservations_list.append(pydentic_models.ReserveOUT(
                    id=reservation.id,
                    customer_name=reservation.customer_name,
                    table_id=reservation.table_id,
                    reservation_time=reservation.reservation_time,
                    duration_minutes=reservation.duration_minutes
                ))
            return reservations_list

    async def add_reservation(self, reserve_data: pydentic_models.ReserveCreate) -> pydentic_models.ReserveOUT:
        logger.info("Request to add new reservation")

        if reserve_data.reservation_time < datetime.now():
            raise HTTPException(status_code=400, detail="Нельзя забронировать столик в прошлом")

        async with self.db.session_maker() as session:
            table_request = select(db_models.Table).where(db_models.Table.id == reserve_data.table_id)
            cursor = await session.execute(table_request)
            table = cursor.scalar_one_or_none()

            if not table:
                raise HTTPException(status_code=404, detail=f"Столик c id {reserve_data.table_id} не найден")

            desired_time_start = reserve_data.reservation_time
            desired_time_end = desired_time_start + timedelta(minutes=reserve_data.duration_minutes)

            reserve_request = select(db_models.Reservation).where(
                db_models.Reservation.table_id == reserve_data.table_id
            )
        reservation_result = await session.execute(reserve_request)
        existing_reservations = reservation_result.scalars().all()

        for reservation in existing_reservations:
            booked_start = reservation.reservation_time
            booked_end = booked_start + timedelta(minutes=reservation.duration_minutes)
            if desired_time_start < booked_end and desired_time_end > booked_start:
                raise HTTPException(status_code=400, detail="Столик на это время уже забронирован")

            new_reservation = db_models.Reservation(**reserve_data.model_dump())
            session.add(new_reservation)
            await session.commit()

            await session.refresh(new_reservation)

            return pydentic_models.ReserveOUT.model_validate(new_reservation)

    async def delete_reservation(self, reserve_id: int) -> None:
        logger.info("Request to delete the reservation")
        async with self.db.session_maker() as session:
            delete_request = select(db_models.Reservation).where(db_models.Reservation.id == reserve_id)
            cursor = await session.execute(delete_request)
            existing_reservation = cursor.scalar_one_or_none()

            if not existing_reservation:
                raise HTTPException(status_code=404, detail="Бронь не найдена")

            await session.delete(existing_reservation)
            await session.commit()
        logger.info("reservation deleted")


table_controller: TableController | None = None


def get_table_controller() -> TableController:
    assert table_controller is not None, "Table controller not initialized"
    return table_controller


reserve_controller: ReservationController | None = None


def get_reserve_controller() -> ReservationController:
    assert reserve_controller is not None, "Reservation controller not initialized"
    return reserve_controller
