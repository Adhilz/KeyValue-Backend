from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name:str

class DepartmentUpdate(BaseModel):
    name:str


class DepartmentResponse(BaseModel):
    id:int
    name:str
    model_config={
        "from_attributes":True
        }