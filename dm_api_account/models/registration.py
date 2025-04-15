from pydantic import BaseModel, Field

class Registration(BaseModel):
    login: str = Field(description="User login")
    email: str = Field(description="User email")
    password: str = Field(description="User password")