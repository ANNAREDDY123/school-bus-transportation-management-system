from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.bus import Bus
from schemas.bus import BusCreate, BusUpdate
from services.transport_service import (
    duplicate_bus_number_exists,
    valid_bus_status
)

router = APIRouter(
    prefix="/buses",
    tags=["Buses"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_bus(
    bus: BusCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Bus).filter(
        Bus.bus_number == bus.bus_number
    ).first()

    if duplicate_bus_number_exists(existing):
        raise HTTPException(
            status_code=400,
            detail="Bus number already exists."
        )

    if not valid_bus_status(bus.status):
        raise HTTPException(
            status_code=400,
            detail="Invalid bus status."
        )

    db_bus = Bus(**bus.model_dump())

    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)

    return db_bus


@router.get("/")
def get_buses(
    route_name: str = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Bus)

    if route_name:
        query = query.filter(
            Bus.route_name == route_name
        )

    if status:
        query = query.filter(
            Bus.status == status
        )

    total = query.count()

    buses = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": buses
    }


@router.get("/{bus_id}")
def get_bus(
    bus_id: int,
    db: Session = Depends(get_db)
):

    bus = db.query(Bus).filter(
        Bus.id == bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    return bus


@router.put("/{bus_id}")
def update_bus(
    bus_id: int,
    bus: BusUpdate,
    db: Session = Depends(get_db)
):

    db_bus = db.query(Bus).filter(
        Bus.id == bus_id
    ).first()

    if not db_bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    duplicate = db.query(Bus).filter(
        Bus.bus_number == bus.bus_number,
        Bus.id != bus_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Bus number already exists."
        )

    if not valid_bus_status(bus.status):
        raise HTTPException(
            status_code=400,
            detail="Invalid bus status."
        )

    for key, value in bus.model_dump().items():
        setattr(db_bus, key, value)

    db.commit()
    db.refresh(db_bus)

    return db_bus


@router.delete("/{bus_id}")
def delete_bus(
    bus_id: int,
    db: Session = Depends(get_db)
):

    bus = db.query(Bus).filter(
        Bus.id == bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    db.delete(bus)
    db.commit()

    return {
        "message": "Bus deleted successfully."
    }
