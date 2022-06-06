from utils.const import ISBN_DESCRIPTION
from typing import Optional, List
from sqlmodel import Field, SQLModel

class JWTUser(SQLModel, table=True):
    username: str = Field(default=None, primary_key=True)
    password: str
    disabled: bool = False
    role: str = None