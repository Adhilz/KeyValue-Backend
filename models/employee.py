from datetime import datetime
import enum
from typing import Optional

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.employee_department import EmployeeDepartment
from models.address import Address
from models.entity import Entity


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None

    return value.isoformat()


class EmployeeRole(str, enum.Enum):
    UI = "UI"
    UX = "UX"
    DEVELOPER = "Developer"
    HR = "HR"


class EmployeeStatus(str, enum.Enum):
    Probation = "Probation"
    Active = "Active"
    Inactive = "Inactive"


class Employee(Entity):
    __abstract__ = False
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )
    role: Mapped[EmployeeRole] = mapped_column(
        Enum(
            EmployeeRole,
            name="employeerole",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )
    age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )
    status: Mapped[EmployeeStatus] = mapped_column(
        Enum(
            EmployeeStatus,
            name="employeestatus",
            values_callable=lambda enum_cls: [e.value for e in enum_cls],
        ),
        nullable=False,
        server_default=EmployeeStatus.Probation.value,
    )

    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    addresses: Mapped[list["Address"]] = relationship(
        "Address",
        back_populates="employee",
        cascade="all, delete-orphan",
    )
    departments: Mapped[list["Department"]] = relationship(  # noqa:F821
        "Department",
        secondary=EmployeeDepartment.__table__,
        back_populates="employees",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=True,
    )

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    # employee_department = relationship(
    # "EmployeeDepartment",
    # back_populates="e",
    # cascade="all, delete-orphan",
    # )
    # # def to_api_dict(self) -> dict[str, Any]:
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "email": self.email,
    #         "age": self.age,

    #         "created_at": _datetime_to_iso(self.created_at),
    #         "updated_at": _datetime_to_iso(self.updated_at),
    #         "deleted_at": _datetime_to_iso(self.deleted_at),
    #     }
