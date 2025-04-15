from pydantic import BaseModel, Field
from typing import Optional


class UserEnvelope(BaseModel):
    resource: Optional[dict] = Field(description="User resource")
    metadata: Optional[dict] = Field(description="Additional metadata")