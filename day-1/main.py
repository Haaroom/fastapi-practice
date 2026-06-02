from fastapi import FastAPI
from database import create_db_and_tables
from schema import StudentCreate, StudentRead

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
@app.post('/create-student',response_model=StudentCreate)
def create_student(student: StudentCreate):
    return student