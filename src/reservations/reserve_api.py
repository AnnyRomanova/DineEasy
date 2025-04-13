import logging

from fastapi import APIRouter, Depends

from reservations.reserve_controllers import (
    ReservationController,
    get_reserve_controller,
)
from reservations.reserve_models import ReserveOUT, ReserveCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/reservations/", tags=["Reservations"], response_model=list[ReserveOUT])
async def get_reserve_list(
    reserve_controller: ReservationController = Depends(get_reserve_controller),
) -> list[ReserveOUT]:
    reservations = await reserve_controller.get_reserve_list()
    return reservations


@router.post(
    "/reservations/", tags=["Reservations"], status_code=201, response_model=ReserveOUT
)
async def create_reservation(
    new_reserve: ReserveCreate,
    reserve_controller: ReservationController = Depends(get_reserve_controller),
) -> ReserveOUT:
    reservation = await reserve_controller.add_reservation(new_reserve)
    return reservation


@router.delete("/reservations/{reserve_id}", tags=["Reservations"], status_code=204)
async def delete_reservation(
    reserve_id: int,
    reserve_controller: ReservationController = Depends(get_reserve_controller),
) -> None:
    await reserve_controller.delete_reservation(reserve_id)
