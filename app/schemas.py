from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime, time
from sqlalchemy.orm import Session
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
class InstructorInput(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., description="Raw password. It will be hashed using bcrypt before storing.")

    @validator("password", pre=True)
    def hash_password(cls, value: str) -> str:
        hashed = bcrypt.generate_password_hash(value).decode("utf-8")
        return hashed

class InstructorSchema(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True

class CourseInput(BaseModel):
    title: str
    description: str
    instructorId: int
    startTime: time
    endTime: time

class CourseSchema(BaseModel):
    id: int
    title: str
    description: str
    instructorId: int
    startTime: time
    endTime: time
    is_deleted: Optional[bool] = False

    class Config:
        from_attributes = True

class CourseWithInstructor(CourseSchema):
    instructor: InstructorSchema

class InstructorWithCourses(InstructorSchema):
    courses: CourseSchema
