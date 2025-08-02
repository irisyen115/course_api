from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models.course import Course
from schemas import CourseInput
from fastapi import HTTPException
from datetime import datetime


def list_courses(db: Session, start: int, limit: int):
    total = db.query(func.count(Course.id)).scalar()
    if start > total and total != 0:
        raise HTTPException(status_code=404, detail="Course index out of range")

    Courses = (
        db.query(Course)
        .options(joinedload(Course.instructor))
        .order_by(Course.id)
        .offset(start - 1)
        .limit(limit)
        .all()
    )

    return total, Courses


def list_instructor_courses(db: Session, instructor_id: int, start: int, limit: int):
    instructor = db.query(instructor).filter_by(id=instructor_id).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor not found")

    total = db.query(func.count(Course.id)).filter_by(instructorId=instructor_id).scalar()
    if start > total and total != 0:
        raise HTTPException(status_code=404, detail="Course index out of range")

    Courses = (
        db.query(Course)
        .filter_by(instructorId=instructor_id)
        .order_by(Course.id)
        .offset(start - 1)
        .limit(limit)
        .all()
    )

    return total, Courses, instructor


def create_course(db: Session, data: CourseInput):
    instructor = db.query(instructor).filter_by(id=data.instructorId).first()
    if not instructor:
        raise HTTPException(status_code=400, detail="Instructor not found")

    Course = Course(**data.model_dump())
    db.add(Course)
    db.commit()
    db.refresh(Course)
    return Course


def update_course(db: Session, Course_id: int, data: CourseInput):
    Course = db.query(Course).filter_by(id=Course_id).first()
    if not Course:
        raise HTTPException(status_code=404, detail="Course not found")

    for key, value in data.model_dump().items():
        setattr(Course, key, value)
    db.commit()
    db.refresh(Course)
    return Course


def delete_course(db: Session, Course_id: int):
    Course = db.query(Course).filter(Course.id == Course_id, Course.is_deleted == False).first()
    if not Course:
        raise HTTPException(status_code=404, detail="Course not found or already deleted")
    Course.is_deleted = True
    Course.deleted_at = datetime.utcnow()
    db.commit()
