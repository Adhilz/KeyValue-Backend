from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.entity import Entity


class Department(Entity):
    __tablename__ = "departments"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
    employee_department = relationship(
        "EmployeeDepartment", back_populates="department"
    )
