from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from schemas import InstructorSchema, InstructorInput
from services import instructor_service
from models.database import get_db
from fastapi import HTTPException

router = APIRouter()

@router.get("/instructors", response_model=dict)
def list_instructors(start: int = Query(1, ge=1), db: Session = Depends(get_db)):
    limit = 2
    total, instructors = instructor_service.list_instructors(db, start, limit)
    if not instructors:
        raise HTTPException(status_code=404, detail="Instructor not found")
    return {
        "items": [InstructorSchema.from_orm(i) for i in instructors],
        "start": start,
        "limit": limit,
        "total": total,
    }


@router.post("/instructors", response_model=InstructorSchema, status_code=201)
def create_instructor(data: InstructorInput, db: Session = Depends(get_db)):
    return instructor_service.create_instructor(db, data)
