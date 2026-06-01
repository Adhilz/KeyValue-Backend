from dataclasses import dataclass
import logging
from typing import TypedDict

from employees.router import router as employee_router
from auth.router import router as auth_router
from departments.router import router as department_router
from addresses.router import router as address_router
from fastapi import FastAPI
from EmployeeDepartment.router import router as employee_department_router
from exceptions.handlers import register_exception_handlers

from fastapi.middleware.cors import CORSMiddleware
from config import setting

from middleware.logger import RequestLoggingMiddleware



from models.employee import Employee

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)



app = FastAPI(
    title="Employee CRUD API with FastAPI",
    description="A simple API for managing employee records.",
    version="1.0.0",
    
)
register_exception_handlers(app)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
employees: list[dict] = []


@dataclass
class EmployeeCreate:
    FirstName: str
    LastName: str
    email: str
    department: str
    salary: float
    hire_date: str
    is_deleted: bool = False


class EmployeePublic(TypedDict):
    id: int
    FirstName: str
    LastName: str
    email: str
    department: str
    salary: float
    hire_date: str
    is_deleted: bool

"""Adding Router for create """
app.include_router(employee_router)
app.include_router(auth_router)
app.include_router(department_router)
app.include_router(address_router)
app.include_router(employee_department_router)
@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": setting.app_env, "debug": setting.debug}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000,reload=True)

