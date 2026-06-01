from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity


class EmployeeDepartment(Entity):
    __tablename__="employee_department"
    dept_id:Mapped[int]=mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )
    emp_id:Mapped[int]=mapped_column(
        ForeignKey("employees.id"),
        nullable=False
    )
    employee=relationship(
        "Employee",
        back_populates="employee_department"
        
    )
    department=relationship(
        "Department",
        back_populates="employee_department"
    )