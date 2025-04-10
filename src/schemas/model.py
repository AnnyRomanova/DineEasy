from datetime import datetime

from pydantic import BaseModel, Field

# проверка входящих данных о столике от пользователя
class TableCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    seats: int = Field(ge=1, le=30)
    location: str = Field(min_length=2, max_length=100)

    model_config = {
        "from_attributes": True
    }

# проверка исходящих данных о столике
class TableOUT(TableCreate):
    id: int

    model_config = {
        "from_attributes": True
    }

# проверка входящих данных о бронировании от пользователя
class ReserveCreate(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    table_id: int
    reservation_time: datetime = Field(
        description="Дата и время бронирования в формате ISO 8601",
        json_schema_extra={
            "example": "2025-12-31T23:59:59",
        }
    )
    duration_minutes: int = Field(ge=60, le=180)

    model_config = {
        "from_attributes": True
    }

# проверка исходящих данных о бронировании
class ReserveOUT(ReserveCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
