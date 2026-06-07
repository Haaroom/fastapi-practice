from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
class Enrollment(SQLModel, table=True):
    student_id: int = Field(
        foreign_key="student.id",
        primary_key=True
    )
    course_id: int = Field(
        foreign_key="course.id",
        primary_key=True
    )
class Student(SQLModel, table=True):
    __tablename__ = "student"
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    name: str
    age: int
    email: str
    courses: list["Course"] = Relationship(
        back_populates="students",
        link_model=Enrollment
    )
class Teacher(SQLModel, table=True):
    __tablename__ = "teacher"
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    name: str
    email: str
    department: str
    courses: list["Course"] = Relationship(
        back_populates="teacher"
    )
class Course(SQLModel, table=True):
    __tablename__ = "course"
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    title: str
    credits: int
    department: str
    teacher_id: int | None = Field(
        default=None,
        foreign_key="teacher.id"
    )
    teacher: Optional["Teacher"] = Relationship(
        back_populates="courses"
    )
    students: list["Student"] = Relationship(
        back_populates="courses",
        link_model=Enrollment
    )