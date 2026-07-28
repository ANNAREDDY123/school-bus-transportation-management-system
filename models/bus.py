from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from database import Base


class Bus(Base):

    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)

    bus_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    driver_name = Column(
        String(100),
        nullable=False
    )

    route_name = Column(
        String(100),
        nullable=False
    )

    total_seats = Column(
        Integer,
        nullable=False
    )

    status = Column(
        String(20),
        nullable=False,
        default="Active"
    )
