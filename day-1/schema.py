from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: int


class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int

class StudentUpdate(BaseModel):
    id :int 
    name :str |None =None 
    email:EmailStr|None = None 
    age : int | None = None 