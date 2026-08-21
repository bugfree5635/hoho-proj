from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):

    name: str

    email: str

    department: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "name": "Henry",
                    "email": "henry@example.com",
                    "department": "Engineering",
                }
            ]
        }
    )


class EmployeeResponse(BaseModel):

    id: int

    name: str

    email: str

    department: str

    model_config = ConfigDict(from_attributes=True)
