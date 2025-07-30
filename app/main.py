from fastapi import FastAPI, APIRouter, HTTPException, Path, status
from typing import List
import uuid
from fastapi import Depends
from sqlalchemy.orm import Session
import uuid
from fastapi.openapi.utils import get_openapi
from models import Instructor, Course
from database import get_db
from schemas import InstructorSchema, CourseSchema, InstructorInput, CourseInput, CourseWithInstructor
from database import engine
from models import Base
from fastapi import Query
from sqlalchemy import func
from typing import List
from sqlalchemy.orm import joinedload
from datetime import datetime

router = APIRouter()

app = FastAPI(
    title="選課清單",
    version="1.0.0",
    docs_url="/docs/",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["servers"] = [
        {"url": "https://irisyen115.synology.me/course-api"},
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.get("/courses", response_model=dict)
def list_courses(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(2, ge=1, le=100)  # 原本是限制最多2筆，這裡設為預設 2 筆
):
    total = db.query(func.count(Course.id)).scalar()
    courses = (
        db.query(Course)
        .options(joinedload(Course.instructor))  # 預先載入 instructor，避免懶加載錯誤
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    if not courses:
        raise HTTPException(status_code=404, detail="Course not found")

    return {
        "items": [CourseWithInstructor.from_orm(c) for c in courses],
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": (total + per_page - 1) // per_page
    }

@app.get("/instructors", response_model=List[InstructorSchema])
def list_instructors(db: Session = Depends(get_db)):
    return db.query(Instructor).limit(2).all()

@app.get("/instructor/{instructorId}/courses", response_model=List[CourseSchema])
def list_instructor_courses(instructorId: str = Path(...), db: Session = Depends(get_db)):
    return db.query(Course).filter(Course.instructorId == instructorId).limit(2).all()

@app.post("/course", response_model=CourseSchema, status_code=201)
def create_course(data: CourseInput, db: Session = Depends(get_db)):
    instructor = db.query(Instructor).filter(Instructor.id == data.instructorId).first()
    if not instructor:
        raise HTTPException(status_code=400, detail="Instructor not found")

    course_id = "course_" + str(uuid.uuid4())
    course = Course(id=course_id, is_deleted=False,**data.model_dump())
    db.add(course)
    db.commit()
    db.refresh(course)
    return course

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

@app.post("/instructor", response_model=InstructorSchema, status_code=201)
def create_instructor(data: InstructorInput, db: Session = Depends(get_db)):
    existing = db.query(Instructor).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    instructor_id = "instr_" + str(uuid.uuid4())
    instructor = Instructor(id=instructor_id, **data.model_dump())

    try:
        db.add(instructor)
        db.commit()
        db.refresh(instructor)
        return instructor
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.put("/course/{courseId}", response_model=CourseSchema)
def update_course(courseId: str, data: CourseInput, db: Session = Depends(get_db)):
    course = db.query(Course).filter_by(id=courseId).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in data.model_dump().items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@app.delete("/course/{courseId}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(courseId: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == courseId, Course.is_deleted == False).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or already deleted")
    course.is_deleted = True
    course.deleted_at = datetime.utcnow()
    db.commit()
