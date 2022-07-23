from dataclasses import dataclass

from pydantic import BaseModel, EmailStr, Field


class ApplicationCreate(BaseModel):

    phone: str = Field(..., regex=r'^(\+)[1-9][0-9\-().]{9,15}$')
    email: EmailStr
    text: str


@dataclass
class ApplicationFilter(object):

    phone: str = ''
    email: str = ''
