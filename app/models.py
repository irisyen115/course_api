from sqlalchemy import Column, String, Text, ForeignKey, Integer, Boolean, DateTime
from sqlalchemy.orm import declarative_base, relationship
import uuid
from database import engine
from sqlalchemy import Index
from sqlalchemy.sql import text

Base = declarative_base()

class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    courses = relationship("Course", back_populates="instructor")

class Student(Base):
    __tablename__ = "students"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    enrollments = relationship("Enrollment", back_populates="student")

class Course(Base):
    __tablename__ = "courses"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    instructorId = Column(String, ForeignKey("instructors.id"), nullable=False, index=True)
    startTime = Column(Integer, nullable=False)
    endTime = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default=text('false'), index=True)
    deleted_at = Column(DateTime, nullable=True)

    instructor = relationship("Instructor", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course", cascade="all, delete-orphan")

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    studentId = Column(String, ForeignKey("students.id"), nullable=False)
    courseId = Column(String, ForeignKey("courses.id"), nullable=False)

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    __table_args__ = (
        Index("ix_enrollment_student_course", "studentId", "courseId", unique=True),
    )


class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    courseId = Column(String, ForeignKey("courses.id"), nullable=False, index=True)
    weekday = Column(Integer, nullable=False, index=True)   # 1=Monday, 7=Sunday
    startTime = Column(Integer, nullable=False) # 例如 900 表示 09:00
    endTime = Column(Integer, nullable=False)   # 例如 1030 表示 10:30

    course = relationship("Course", back_populates="schedules")

Base.metadata.create_all(bind=engine)