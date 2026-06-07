from pydantic import BaseModel, EmailStr
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    age: int
class StudentRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    age: int | None = None
class CourseCreate(BaseModel):
    title: str
    credits: int
    department: str
    teacher_id: int | None = None
class CourseRead(BaseModel):
    id: int
    title: str
    credits: int
    department: str
    teacher_id: int | None = None
class CourseUpdate(BaseModel):
    title: str | None = None
    credits: int | None = None
    department: str | None = None
    teacher_id: int | None = None
class TeacherCreate(BaseModel):
    id:int | None = None 
    name :str 
    email :EmailStr
    department :str
class TeacherRead(BaseModel):
    id:int 
    name :str 
    email :EmailStr
    department :str
class TeacherUpdate(BaseModel):
    id:int  
    name :str | None = None 
    email :EmailStr | None = None 
    department :str | None = None 

    