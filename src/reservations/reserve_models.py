from datetime import datetime

from pydantic import BaseModel, Field


class ReserveCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    table_id: int
    reservation_time: datetime = Field(
        description="Дата и время бронирования (ISO 8601 с timezone)",
        json_schema_extra={"example": "2025-12-31T23:59:59+00:00"},
    )
    duration_minutes: int

    model_config = {"from_attributes": True}


class ReserveOUT(ReserveCreate):
    id: int

    model_config = {"from_attributes": True}
