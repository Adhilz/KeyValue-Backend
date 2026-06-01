from pydantic import BaseModel


class EmployeeDepartment(BaseModel):
    emp_id: int
    dept_id: int
    model_config = {"form_attributes": True}


class EmployeeDepartmentCreate(BaseModel):
    emp_id: int
    dept_id: int
