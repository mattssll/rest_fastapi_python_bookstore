from pydantic import BaseModel
import enum


class Role(str, enum.Enum):
    admin: str = "admin"
    personel: str = "personel"


class User(BaseModel):
    name: str
    password: str
    mail: str = None  # we can add a regex="addregexexpression", to validate field
    role: Role
