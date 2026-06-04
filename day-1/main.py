from fastapi import FastAPI, HTTPException, Depends,Emailstr
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Student
from schema import StudentCreate, StudentRead,StudentUpdate

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# CREATE
@app.post("/create-student", response_model=StudentRead)
def create_student(
    student: StudentCreate,
    session: Session = Depends(get_session)
):

    db_student = Student(
        name=student.name,
        age=student.age,
        grade=student.grade
    )

    session.add(db_student)
    session.commit()
    session.refresh(db_student)

    return db_student


# READ ALL
@app.get("/students", response_model=list[StudentRead])
def read_students(
    session: Session = Depends(get_session),
    grade:str | None = None,
    min_age:int|None = None,
    name:str|None = None ,
    max_age:int |None = None 
):
    statement = select(Student)
    if grade:
        statement=statement.where(Student.grade==grade)
    if min_age:
        statement=statement.where(Student.age>=min_age)
    if max_age:
        statement = statement.where(Student.age <= max_age)
    if name:
        statement = statement.where(Student.age.contains(name))
    students = session.exec(
    statement
    ).all()
    return students


# READ ONE
@app.get("/students/{student_id}", response_model=StudentRead)
def read_student(
    student_id: int,
    session: Session = Depends(get_session)
):

    student = session.exec(
        select(Student).where(
            Student.id == student_id
        )
    ).first()

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# UPDATE
@app.put("/students/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    student: StudentCreate,
    session: Session = Depends(get_session)
):

    existing_student = session.exec(
        select(Student).where(
            Student.id == student_id
        )
    ).first()

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.grade = student.grade

    session.add(existing_student)
    session.commit()
    session.refresh(existing_student)

    return existing_student


# DELETE
@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    session: Session = Depends(get_session)
):

    existing_student = session.exec(
        select(Student).where(
            Student.id == student_id
        )
    ).first()

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    session.delete(existing_student)
    session.commit()
    return {
        "detail": "Student deleted successfully"
    }
#Update 
@app.patch(
    "/students/{id}",
    response_model=StudentRead
)
def update_student(
    id: int,
    student : StudentUpdate,
    session: Session = Depends(get_session),
):
    student = session.exec(
        select(Student).where(
            Student.id == id
        )
    ).first()
    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )
    update_data = student.model_dump(
    exclude_unset=True
)
    for key,value in update_data.items():
        setattr(student,key,value)
    session.add(student)
    session.commit()
    session.refresh(student)

    return student