from fastapi import APIRouter,Depends,HTTPException
from models import Teacher
from schema import TeacherCreate,TeacherRead,TeacherUpdate
from sqlmodel import Session,select
from database import get_session 
teacher_router = APIRouter(prefix="/teachers",tags=["Teachers"])
@teacher_router.post(
    "/",
    response_model=TeacherRead
)
def create_teacher(
    teacher: TeacherCreate,
    session: Session = Depends(get_session)
):

    db_teacher = Teacher(
        name=teacher.name,
        email=teacher.email,
        department=teacher.department
    )

    session.add(db_teacher)
    session.commit()
    session.refresh(db_teacher)

    return db_teacher


@teacher_router.get(
    "/",
    response_model=list[TeacherRead]
)
def get_teachers(
    session: Session = Depends(get_session)
):

    teachers = session.exec(
        select(Teacher)
    ).all()

    return teachers


@teacher_router.get(
    "/{teacher_id}",
    response_model=TeacherRead
)
def get_teacher(
    teacher_id: int,
    session: Session = Depends(get_session)
):

    teacher = session.get(
        Teacher,
        teacher_id
    )

    if not teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    return teacher


@teacher_router.put(
    "/{teacher_id}",
    response_model=TeacherRead
)
def update_teacher(
    teacher_id: int,
    teacher: TeacherCreate,
    session: Session = Depends(get_session)
):

    existing_teacher = session.get(
        Teacher,
        teacher_id
    )

    if not existing_teacher:
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    existing_teacher.name = teacher.name
    existing_teacher.email = teacher.email
    existing_teacher.department = teacher.department

    session.commit()
    session.refresh(existing_teacher)

    return existing_teacher


@teacher_router.patch(
    "/{teacher_id}",
    response_model=TeacherRead
)
def patch_teacher(
    teacher_id: int,
    teacher_update: TeacherUpdate,session: Session = Depends(get_session)):
    teacher = session.get(Teacher,teacher_id)
    if not teacher:
        raise HTTPException(status_code=404,detail="Teacher not found")
    update_data = teacher_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(teacher,key,value)
    session.commit()
    session.refresh(teacher)
    return teacher
@teacher_router.delete("/{teacher_id}")
def delete_teacher(teacher_id: int,session: Session = Depends(get_session)):
    teacher = session.get(Teacher,teacher_id)
    if not teacher:
        raise HTTPException(status_code=404,detail="Teacher not found")
    session.delete(teacher)
    session.commit()
    return {
        "message": "Teacher deleted successfully"
    }