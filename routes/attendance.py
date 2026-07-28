from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.attendance import Attendance
from models.bus import Bus
from models.student import Student
from schemas.attendance import AttendanceCreate
from services.transport_service import (
    duplicate_attendance_exists,
    valid_attendance_status
)

router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/")
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == attendance.student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    bus = db.query(Bus).filter(
        Bus.id == attendance.bus_id
    ).first()

    if not bus:

        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    if student.bus_id != attendance.bus_id:

        raise HTTPException(
            status_code=400,
            detail="Student is not assigned to this bus."
        )

    if not valid_attendance_status(
        attendance.pickup_status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid pickup status."
        )

    if not valid_attendance_status(
        attendance.drop_status
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid drop status."
        )

    existing = db.query(Attendance).filter(
        Attendance.student_id == attendance.student_id,
        Attendance.travel_date == attendance.travel_date
    ).first()

    if duplicate_attendance_exists(existing):

        raise HTTPException(
            status_code=400,
            detail="Attendance already marked for this student today."
        )

    db_attendance = Attendance(
        **attendance.model_dump()
    )

    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)

    return db_attendance


@router.get("/")
def get_attendance(
    travel_date: date = None,
    student_id: int = None,
    bus_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Attendance)

    if travel_date:

        query = query.filter(
            Attendance.travel_date == travel_date
        )

    if student_id:

        query = query.filter(
            Attendance.student_id == student_id
        )

    if bus_id:

        query = query.filter(
            Attendance.bus_id == bus_id
        )

    total = query.count()

    records = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": records
    }


@router.get("/reports/daily")
def daily_attendance_report(
    travel_date: date,
    db: Session = Depends(get_db)
):

    records = db.query(Attendance).filter(
        Attendance.travel_date == travel_date
    ).all()

    return {
        "travel_date": travel_date,
        "total_records": len(records),
        "data": records
    }


@router.get("/{attendance_id}")
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db)
):

    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:

        raise HTTPException(
            status_code=404,
            detail="Attendance record not found."
        )

    return attendance
