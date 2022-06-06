import enum
from typing import Optional, List
from sqlmodel import Field, SQLModel


class Role(str, enum.Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(SQLModel, table=True):
    mail: str = Field(default=None, primary_key=True)
    name: str
    password: str
    role: Role
