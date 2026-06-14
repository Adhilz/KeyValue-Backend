from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic import EmailStr

from addresses.schemas import AddressCreate, AddressResponse
from departments.schemas import DepartmentCreate, DepartmentResponse
from models.employee import EmployeeRole


class EmployeeCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")
    name: str
    email: EmailStr
    age: int | None = Field(ge=0, le=150, default=None)
    password: str = Field(min_length=6)
    role: EmployeeRole
    status: str
    addresses: AddressCreate | None = None
    department: DepartmentCreate | None = None


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr
    age: int | None
    addresses: list[AddressResponse] = []
    departments: list[DepartmentResponse] = []
    role: EmployeeRole
    status: str


class EmployeeUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    name: str | None = None
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)
    status: str
    role: EmployeeRole


class EmployeeFullUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")
    name: str
    email: EmailStr
    age: int | None = Field(default=None, ge=0, le=150)
    status: str
    role: EmployeeRole


class EmployeeidResponse(EmployeeResponse):
    created_at: datetime
    updated_at: datetime
