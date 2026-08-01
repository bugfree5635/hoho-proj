from pydantic import BaseModel, ConfigDict



class EmployeeCreate(BaseModel):

    name: str

    email: str

    department: str



class EmployeeResponse(BaseModel):

    id: int

    name: str

    email: str

    department: str



    model_config = ConfigDict(
        from_attributes=True
    )