from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Student(Base):

    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    student_name = Column(
        String(100),
        nullable=False
    )

    admission_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    class_name = Column(
        String(50),
        nullable=False
    )

    pickup_location = Column(
        String(150),
        nullable=False
    )

    bus_id = Column(
        Integer,
        ForeignKey("buses.id"),
        nullable=False
    )
