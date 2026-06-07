from fastapi import APIRouter,Depends,HTTPException
from models import Course
from schema import CourseCreate,CourseRead,CourseUpdate
from sqlmodel import Session,select
from database import get_session 
courses_router = APIRouter(prefix="/teachers",tags=["Teachers"])
@courses_router.post("/",
          response_model=CourseRead)
def create_course(
    course: CourseCreate,
    session: Session = Depends(get_session)
):
    db_course = Course(
        title=course.title,
        credits=course.credits,
        department=course.department,
        teacher_id=course.teacher_id
    )
    session.add(db_course)
    session.commit()
    session.refresh(db_course)
    return db_course
@courses_router.get("/",
         response_model=list[CourseRead])
def get_courses(
    session: Session = Depends(get_session)
):
    courses = session.exec(
        select(Course)
    ).all()
    return courses
@courses_router.get("/{course_id}",
         response_model=CourseRead)
def get_course(
    course_id: int,
    session: Session = Depends(get_session)
):
    course = session.get(
        Course,
        course_id
    )
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    return course
@courses_router.put("/{course_id}",
         response_model=CourseRead)
def update_course(
    course_id: int,
    course: CourseCreate,
    session: Session = Depends(get_session)
):
    existing_course = session.get(
        Course,
        course_id
    )
    if not existing_course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    existing_course.title = course.title
    existing_course.credits = course.credits
    existing_course.department = course.department
    existing_course.teacher_id = course.teacher_id
    session.commit()
    session.refresh(existing_course)
    return existing_course
@courses_router.patch("/{course_id}",
           response_model=CourseRead)
def patch_course(
    course_id: int,
    course_update: CourseUpdate,
    session: Session = Depends(get_session)
):
    course = session.get(
        Course,
        course_id
    )
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    update_data = course_update.model_dump(
        exclude_unset=True
    )
    for key, value in update_data.items():
        setattr(course, key, value)
    session.commit()
    session.refresh(course)
    return course
@courses_router.delete("/{course_id}")
def delete_course(
    course_id: int,
    session: Session = Depends(get_session)
):
    course = session.get(
        Course,
        course_id
    )
    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )
    session.delete(course)
    session.commit()
    return {
        "message": "Course deleted successfully"
    }