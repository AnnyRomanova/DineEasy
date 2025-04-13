from pydantic import BaseModel, Field


class TableCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    seats: int = Field(ge=1, le=30)
    location: str = Field(min_length=2, max_length=100)

    model_config = {"from_attributes": True}


class TableOUT(TableCreate):
    id: int

    model_config = {"from_attributes": True}
