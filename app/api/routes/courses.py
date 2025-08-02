from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.orm import Session
from schemas import CourseSchema, CourseInput, CourseWithInstructor
from services import course_service
from models.database import get_db

router = APIRouter()

@router.get("/courses", response_model=dict)
def list_courses(start: int = Query(1, ge=1), db: Session = Depends(get_db)):
    limit = 2
    total, courses = course_service.list_courses(db, start, limit)
    if not courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "items": [CourseWithInstructor.from_orm(c) for c in courses],
        "start": start,
        "limit": limit,
        "total": total,
    }


@router.get("/instructors/{instructorId}/courses", response_model=dict)
def list_instructor_courses(
    instructorId: int = Path(...),
    start: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    limit = 2
    total, courses, instructor = course_service.list_instructor_courses(db, instructorId, start, limit)
    if not courses:
        raise HTTPException(status_code=404, detail="Course not found")
    return {
        "items": [CourseSchema.from_orm(c) for c in courses],
        "total": total,
        "start": start,
        "limit": limit,
        "instructor": {
            "email": instructor.email,
            "name": instructor.name,
        },
    }


@router.post("/courses", response_model=CourseSchema, status_code=201)
def create_course(data: CourseInput, db: Session = Depends(get_db)):
    return course_service.create_course(db, data)


@router.put("/courses/{courseId}", response_model=CourseSchema)
def update_course(courseId: int, data: CourseInput, db: Session = Depends(get_db)):
    return course_service.update_course(db, courseId, data)


@router.delete("/courses/{courseId}", status_code=204)
def delete_course(courseId: int, db: Session = Depends(get_db)):
    course_service.delete_course(db, courseId)
