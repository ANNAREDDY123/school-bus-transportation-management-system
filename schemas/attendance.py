from datetime import date

from pydantic import BaseModel


class AttendanceCreate(BaseModel):

    student_id: int

    bus_id: int

    travel_date: date

    pickup_status: str

    drop_status: str


class AttendanceResponse(AttendanceCreate):

    id: int

    class Config:
        from_attributes = True
