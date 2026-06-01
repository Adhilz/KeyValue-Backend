from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


from models.entity import Entity

if TYPE_CHECKING:
    from models.employee import Employee


class Address(Entity):
    __abstract__ = False
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    employee_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
    )

    line: Mapped[str] = mapped_column(String(100), nullable=False)

    city: Mapped[str] = mapped_column(String(100), nullable=False)

    postal_code: Mapped[str] = mapped_column(String(20), nullable=False)

    country: Mapped[str] = mapped_column(String(100), nullable=False)

    employee: Mapped["Employee"] = relationship(
    "Employee",
    back_populates="addresses",  # ✅ plural
)

    def to_api_dict(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "line": self.line,
            "city": self.city,
            "postal_code": self.postal_code,
            "country": self.country,
        }