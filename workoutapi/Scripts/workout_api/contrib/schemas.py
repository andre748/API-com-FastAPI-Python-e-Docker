from typing import Annotated
from pydantic import BaseModel, UUID4, Field
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        extra = "forbid"
        from_attributes = True

class OutMixin(BaseSchema):
    id: Annotated[UUID4, Field(description="ID único do registro", example="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    created_at: Annotated[datetime, Field(description="Data e hora de criação do registro", example="2023-10-05T14:48:00.000Z")]