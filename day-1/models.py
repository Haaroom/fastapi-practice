from typing import Optional 
from SQLModel import SQLModel, Field
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: int
    email: str
