import logging

from fastapi import APIRouter, Depends

from tables.table_controllers import (
    TableController,
    get_table_controller,
)
from tables.table_models import TableOUT, TableCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/tables/", tags=["Tables"], response_model=list[TableOUT])
async def get_tables_list(
    table_controller: TableController = Depends(get_table_controller),
) -> list[TableOUT]:
    tables = await table_controller.get_tables_list()
    return tables


@router.post("/tables/", tags=["Tables"], status_code=201, response_model=TableOUT)
async def create_table(
    new_table: TableCreate,
    table_controller: TableController = Depends(get_table_controller),
) -> TableOUT:
    table = await table_controller.add_table(new_table)
    return table


@router.delete("/tables/{table_id}", tags=["Tables"], status_code=204)
async def delete_table(
    table_id: int, table_controller: TableController = Depends(get_table_controller)
) -> None:
    await table_controller.delete_table(table_id)
