import logging
from fastapi import HTTPException
from sqlalchemy import select
from db.connector import DatabaseConnector

import tables.table_models as pydentic_models
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
                tables_list.append(
                    pydentic_models.TableOUT(
                        id=table.id,
                        name=table.name,
                        seats=table.seats,
                        location=table.location,
                    )
                )
            return tables_list

    async def add_table(
        self, table_data: pydentic_models.TableCreate
    ) -> pydentic_models.TableOUT:
        logger.info("Request to add new table")
        async with self.db.session_maker() as session:
            table_name_request = select(db_models.Table).where(
                db_models.Table.name == table_data.name
            )
            result = await session.execute(table_name_request)
            table_name = result.scalar_one_or_none()

            if table_name:
                logger.error(f"Table with name {table_data.name} already exists")
                raise HTTPException(
                    status_code=400,
                    detail=f'Столик с именем "{table_data.name}" уже существует',
                )

            new_table = db_models.Table(**table_data.model_dump())
            session.add(new_table)
            await session.commit()

            await session.refresh(new_table)

            return pydentic_models.TableOUT.model_validate(new_table)

    async def delete_table(self, table_id: int) -> None:
        logger.info("Request to delete the table")
        async with self.db.session_maker() as session:
            delete_request = select(db_models.Table).where(
                db_models.Table.id == table_id
            )
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


table_controller: TableController | None = None


def get_table_controller() -> TableController:
    assert table_controller is not None, "Table controller not initialized"
    return table_controller
