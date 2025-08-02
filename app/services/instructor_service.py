from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from models.instructor import Instructor
from schemas import InstructorInput
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


def list_instructors(db: Session, start: int, limit: int):
    total = db.query(func.count(Instructor.id)).scalar()
    if start > total and total != 0:
        raise HTTPException(status_code=404, detail="Instructor index out of range")

    Instructors = (
        db.query(Instructor)
        .options(joinedload(Instructor.courses))
        .order_by(Instructor.id)
        .offset(start - 1)
        .limit(limit)
        .all()
    )

    return total, Instructors


def create_instructor(db: Session, data: InstructorInput):
    existing = db.query(Instructor).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    Instructor = Instructor(**data.model_dump())
    try:
        db.add(Instructor)
        db.commit()
        db.refresh(Instructor)
        return Instructor
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

