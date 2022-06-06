from pydantic import BaseModel
from typing import List, Optional
from sqlmodel import Field, Session, SQLModel, create_engine, select, Relationship


class Author(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    books: List["Book"] = Relationship(back_populates="author")