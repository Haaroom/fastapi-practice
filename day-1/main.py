from select import select
from fastapi import FastAPI,HTTPException
from database import create_db_and_tables,get_session
from schema import StudentCreate, StudentRead
from sqlmodel import Session
from schema import  Student
app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
@app.post('/create-student',response_model=StudentCreate)
def create_student(student: StudentCreate):
    student = Student(
        name=student.name,
        age=student.age,
        grade=student.grade
    )
    with get_session() as session:
        session.add(Student)
        session.commit()
        session.refresh(Student)
    return student
@app.get('/students',response_model=list[StudentRead])
def read_students():
    with get_session() as session:
        students = session.query(Student).all()
    return students
@app.get('/students/{student_id}',response_model=StudentRead)
def read_student(student_id:int):
    with get_session() as session:
        student = session.query(Student).filter(Student.id==student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        return student
@app.put('/students/{student_id}',response_model=StudentRead)
def update_student(student_id:int,student : StudentCreate):
    with get_session() as session:
        existing_student = session.query(Student).exec(select(Student).where(Student.id == student_id)).first()
        if not existing_student:
            raise HTTPException(status_code=404,detail="Student not found")
        existing_student.name = student.name
        existing_student.age = student.age
        existing_student.grade = student.grade
        session.add(existing_student)
        session.commit()
        session.refresh(existing_student)
        return existing_student
@app.delete('/students/{student_id}')
def delete_student(student_id : int ):
    with get_session() as session:
        existing_student = session.exec(select(Student).where(Student.id == student_id)).first()
        if not existing_student:
            raise HTTPException(status_code=404 , detail = " Student not found")
        session.delete(existing_student)
        session.commit()
        session.refresh(existing_student)
        return {"detail": "Student deleted successfully"}
    