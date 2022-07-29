from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class ApplicationCreate(BaseModel):

    phone: str = Field(..., regex=r'^(\+)[1-9][0-9\-().]{9,15}$')
    email: EmailStr
    text: str


class ApplicationRead(BaseModel):

    id: UUID

    phone: str
    email: EmailStr
    text: str

    created_at: datetime
    updated_at: datetime | None
    deleted_at: datetime | None

    class Config(object):
        orm_mode = True


@dataclass
class ApplicationFilter(object):

    phone: str = ''
    email: str = ''
