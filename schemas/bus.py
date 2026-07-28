from pydantic import BaseModel, Field


class BusCreate(BaseModel):

    bus_number: str

    driver_name: str

    route_name: str

    total_seats: int = Field(gt=0)

    status: str


class BusUpdate(BaseModel):

    bus_number: str

    driver_name: str

    route_name: str

    total_seats: int = Field(gt=0)

    status: str


class BusResponse(BusCreate):

    id: int

    class Config:
        from_attributes = True
