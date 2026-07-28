# school-bus-transportation-management-system
Use this for the GitHub repository **Description**:  > **A complete School Bus Transportation Management System built with FastAPI, featuring JWT authentication, role-based authorization, bus and student management, route attendance, search, pagination, and business-rule validations.**
# School Bus Transportation Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Bus Management
- Student Allocation
- Route Attendance
- Bus Capacity Validation
- Student Search
- Bus Filtering
- Daily Attendance Reports
- Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Tech Stack

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn

## Installation

Install dependencies:

pip install -r requirements.txt

Run the application:


uvicorn main:app --reload


Swagger Documentation:


http://127.0.0.1:8000/docs


## Roles

- Admin
- Transport Manager
- Parent

## Business Rules

- Bus number must be unique
- Admission number must be unique
- Bus capacity cannot exceed total seats
- Students cannot be assigned to inactive buses
- Attendance can be marked only once per student per day
- Total seats must be greater than zero

## API Modules

- Authentication
- Buses
- Students
- Attendance
- Reports & Search
