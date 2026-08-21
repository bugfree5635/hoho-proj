from pydantic import BaseModel, ConfigDict


class UserCreate(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "examples": [
                {
                    "username": "henry",
                    "password": "example-password",
                }
            ]
        }
    )


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
