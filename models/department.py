from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.employee_department import EmployeeDepartment
from models.entity import Entity


class Department(Entity):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    employees: Mapped[list["Employee"]] = relationship(  # noqa:F821
        "Employee",
        secondary=EmployeeDepartment.__table__,
        back_populates="departments",
    )
