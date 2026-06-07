from fastapi import FastAPI
from database import create_db_and_tables
from routes.students import student_router
from routes.courses import course_router
from routes.teacher import teacher_router

app = FastAPI()
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(course_router)
