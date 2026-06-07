from fastapi import APIRouter,Depends,HTTPException
from models import Student
from schema import StudentCreate,StudentRead,StudentUpdate
from sqlmodel import Session,select
from database import get_session 

student_router = APIRouter(prefix='/students',tags=["Students"])
@student_router.post("/", response_model=StudentRead)
def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session)
):
    db_student = Student(
        name=student.name,
        email=student.email,
        age=student.age
    )
    session.add(db_student)
    session.commit()
    session.refresh(db_student)
    return db_student
@student_router.get("/", response_model=list[StudentRead])
def get_students(
    session: Session = Depends(get_session),
    min_age: int | None = None,
    max_age: int | None = None,
    name: str | None = None
):
    statement = select(Student)
    if min_age:
        statement = statement.where(
            Student.age >= min_age
        )
    if max_age:
        statement = statement.where(
            Student.age <= max_age
        )
    if name:
        statement = statement.where(
            Student.name.contains(name)
        )
    students = session.exec(statement).all()
    return students
@student_router.get("/{student_id}",
         response_model=StudentRead)
def get_student(
    student_id: int,
    session: Session = Depends(get_session)
):
    student = session.get(
        Student,
        student_id
    )
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    return student
@student_router.put("/{student_id}",
         response_model=StudentRead)
def update_student(
    student_id: int,
    student: StudentCreate,
    session: Session = Depends(get_session)
):
    existing_student = session.get(
        Student,
        student_id
    )
    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    existing_student.name = student.name
    existing_student.email = student.email
    existing_student.age = student.age
    session.commit()
    session.refresh(existing_student)
    return existing_student
@student_router.patch("/{student_id}",
           response_model=StudentRead)
def patch_student(
    student_id: int,
    student_update: StudentUpdate,
    session: Session = Depends(get_session)
):
    student = session.get(
        Student,
        student_id
    )
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    update_data = student_update.model_dump(
        exclude_unset=True
    )
    for key, value in update_data.items():
        setattr(student, key, value)
    session.commit()
    session.refresh(student)
    return student
@student_router.delete("/{student_id}")
def delete_student(
    student_id: int,
    session: Session = Depends(get_session)
):
    student = session.get(
        Student,
        student_id
    )
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    session.delete(student)
    session.commit()
    return {
        "message": "Student deleted successfully"
    }