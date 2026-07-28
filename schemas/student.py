from pydantic import BaseModel


class StudentCreate(BaseModel):

    student_name: str

    admission_number: str

    class_name: str

    pickup_location: str

    bus_id: int


class StudentUpdate(BaseModel):

    student_name: str

    admission_number: str

    class_name: str

    pickup_location: str

    bus_id: int


class StudentResponse(StudentCreate):

    id: int

    class Config:
        from_attributes = True
