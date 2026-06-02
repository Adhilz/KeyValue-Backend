from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from models.entity import Entity


class EmployeeDepartment(Entity):
    __tablename__ = "employee_department"
    dept_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=False
    )
    emp_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id", ondelete="CASCADE"), nullable=False
    )

    __table_args__ = (UniqueConstraint("emp_id", "dept_id"),)
