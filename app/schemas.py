from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
class InstructorInput(BaseModel):
    name: str
    email: EmailStr
    password: str

class InstructorSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    password: Optional[str] = None

    class Config:
        from_attributes = True

class CourseInput(BaseModel):
    title: str
    description: str
    instructorId: str
    startTime: int
    endTime: int

class CourseSchema(BaseModel):
    id: str
    title: str
    description: str
    instructorId: str
    startTime: int
    endTime: int
    is_deleted: Optional[bool] = False
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CourseWithInstructor(CourseSchema):
    instructor: InstructorSchema
