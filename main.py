from fastapi import FastAPI

from database import Base, engine

from models.user import User
from models.bus import Bus
from models.student import Student
from models.attendance import Attendance

from routes.auth import router as auth_router
from routes.buses import router as buses_router
from routes.students import router as students_router
from routes.attendance import router as attendance_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="School Bus Transportation Management System"
)

app.include_router(auth_router)
app.include_router(buses_router)
app.include_router(students_router)
app.include_router(attendance_router)


@app.get("/")
def home():
    return {
        "message": "School Bus Transportation Management System API"
    }
