from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.connection import get_database
from ..database.models import Employee
from ..schemas.employee import EmployeeCreate, EmployeeResponse

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get(
    "/",
    summary="List employees",
    description="Return all employees stored in the database.",
    response_model=list[EmployeeResponse],
    response_description="A List of employees.",
)
def get_employees(db: Session = Depends(get_database)):

    return db.query(Employee).all()


@router.post(
    "/",
    summary="Create an employee",
    description="Create a new employee record.",
    response_model=EmployeeResponse,
)
def create_employee(employee: EmployeeCreate, db: Session = Depends(get_database)):

    new_employee = Employee(
        name=employee.name, email=employee.email, department=employee.department
    )

    db.add(new_employee)

    db.commit()

    db.refresh(new_employee)

    return new_employee
