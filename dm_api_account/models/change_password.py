from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ChangePassword(BaseModel):
    login: str = Field(description="User login")
    token: Optional[UUID] = Field(description="Password reset token")
    old_password: Optional[str] = Field(description="Old password")
    new_password: str = Field(description="New password")