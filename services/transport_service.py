VALID_BUS_STATUS = [
    "Active",
    "Maintenance",
    "Inactive"
]


VALID_ATTENDANCE_STATUS = [
    "Present",
    "Absent",
    "Pending"
]


def valid_bus_status(status: str):

    return status in VALID_BUS_STATUS


def valid_total_seats(total_seats: int):

    return total_seats > 0


def bus_is_active(bus):

    return bus.status == "Active"


def bus_has_capacity(
    current_students: int,
    total_seats: int
):

    return current_students < total_seats


def duplicate_bus_number_exists(bus):

    return bus is not None


def duplicate_admission_number_exists(student):

    return student is not None


def duplicate_attendance_exists(attendance):

    return attendance is not None


def valid_attendance_status(status: str):

    return status in VALID_ATTENDANCE_STATUS
