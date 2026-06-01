from datetime import datetime
import enum
from typing import Any, Optional

from sqlalchemy import DateTime, Enum, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.address import Address
from models.department import Department
from models.entity import Entity


def _datetime_to_iso(value: datetime | None) -> str | None:
    if value is None:
        return None

    return value.isoformat()

class EmployeeRole(str,enum.Enum):
    UI="UI"
    UX="UX"
    DEVELOPER="Developer"
    HR="HR" 

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
    role: Mapped[EmployeeRole]=mapped_column(
        Enum(EmployeeRole, name="employeerole",values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        server_default=EmployeeRole.DEVELOPER.value,
    )
    age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )


    password_hash:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    addresses: Mapped[list["Address"]] = relationship(
    "Address",
    back_populates="employee",   # ✅ singular
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
    employee_department = relationship(
    "EmployeeDepartment",
    back_populates="employee"
)
    # def to_api_dict(self) -> dict[str, Any]:
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "email": self.email,
    #         "age": self.age,

            

    #         "created_at": _datetime_to_iso(self.created_at),
    #         "updated_at": _datetime_to_iso(self.updated_at),
    #         "deleted_at": _datetime_to_iso(self.deleted_at),
    #     }