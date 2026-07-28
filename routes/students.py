from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.bus import Bus
from models.student import Student
from schemas.student import StudentCreate, StudentUpdate
from services.transport_service import (
    bus_has_capacity,
    bus_is_active,
    duplicate_admission_number_exists
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Student).filter(
        Student.admission_number ==
        student.admission_number
    ).first()

    if duplicate_admission_number_exists(existing):
        raise HTTPException(
            status_code=400,
            detail="Admission number already exists."
        )

    bus = db.query(Bus).filter(
        Bus.id == student.bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    if not bus_is_active(bus):
        raise HTTPException(
            status_code=400,
            detail="Students can only be assigned to active buses."
        )

    current_students = db.query(Student).filter(
        Student.bus_id == student.bus_id
    ).count()

    if not bus_has_capacity(
        current_students,
        bus.total_seats
    ):
        raise HTTPException(
            status_code=400,
            detail="Bus capacity is full."
        )

    db_student = Student(
        **student.model_dump()
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


@router.get("/")
def get_students(
    admission_number: str = None,
    name: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Student)

    if admission_number:
        query = query.filter(
            Student.admission_number ==
            admission_number
        )

    if name:
        query = query.filter(
            Student.student_name.ilike(
                f"%{name}%"
            )
        )

    total = query.count()

    students = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": students
    }


@router.get("/{student_id}")
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    return student


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):

    db_student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not db_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found."
        )

    duplicate = db.query(Student).filter(
        Student.admission_number ==
        student.admission_number,
        Student.id != student_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Admission number already exists."
        )

    bus = db.query(Bus).filter(
        Bus.id == student.bus_id
    ).first()

    if not bus:
        raise HTTPException(
            status_code=404,
            detail="Bus not found."
        )

    if not bus_is_active(bus):
        raise HTTPException(
            status_code=400,
            detail="Students can only be assigned to active buses."
        )

    if db_student.bus_id != student.bus_id:

        current_students = db.query(Student).filter(
            Student.bus_id == student.bus_id
        ).count()

        if not bus_has_capacity(
            current_students,
            bus.total_seats
        ):
            raise HTTPException(
                status_code=400,
                detail="Bus capacity is full."
            )

    for key, value in student.model_dump().items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)

    return db_student
