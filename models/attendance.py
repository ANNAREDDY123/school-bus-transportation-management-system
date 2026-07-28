from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import UniqueConstraint

from database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    bus_id = Column(
        Integer,
        ForeignKey("buses.id"),
        nullable=False
    )

    travel_date = Column(
        Date,
        nullable=False
    )

    pickup_status = Column(
        String(30),
        nullable=False
    )

    drop_status = Column(
        String(30),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "travel_date",
            name="unique_student_daily_attendance"
        ),
    )
