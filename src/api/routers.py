import logging

from fastapi import APIRouter, Depends

from controllers.controllers import TableController, get_table_controller, ReservationController, get_reserve_controller
from schemas.model import TableOUT, TableCreate, ReserveOUT, ReserveCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/tables/",  tags=["Tables"], response_model=list[TableOUT])
async def get_tables_list(
        table_controller: TableController = Depends(get_table_controller)
) -> list[TableOUT]:
    tables = await table_controller.get_tables_list()
    return tables


@router.post("/tables/",  tags=["Tables"], status_code=201, response_model=TableOUT)
async def create_table(new_table: TableCreate,
                       table_controller: TableController = Depends(get_table_controller)) -> TableOUT:
    table = await table_controller.add_table(new_table)
    return table


@router.delete("/tables/{table_id}", tags=["Tables"], status_code=204)
async def delete_table(table_id: int, table_controller: TableController = Depends(get_table_controller)) -> None:
    await table_controller.delete_table(table_id)


@router.get("/reservations/", tags=["Reservations"], response_model=list[ReserveOUT])
async def get_reserve_list(
        reserve_controller: ReservationController = Depends(get_reserve_controller)
) -> list[ReserveOUT]:
    reservations = await reserve_controller.get_reserve_list()
    return reservations


@router.post("/reservations/",  tags=["Reservations"], status_code=201, response_model=ReserveOUT)
async def create_reservation(new_reserve: ReserveCreate,
                       reserve_controller: ReservationController = Depends(get_reserve_controller)) -> ReserveOUT:
    reservation = await reserve_controller.add_reservation(new_reserve)
    return reservation


@router.delete("/reservations/{reserve_id}", tags=["Reservations"], status_code=204)
async def delete_reservation(reserve_id: int, reserve_controller: ReservationController = Depends(get_reserve_controller)) -> None:
    await reserve_controller.delete_reservation(reserve_id)