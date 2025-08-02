from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, DateTime, Boolean, text
from sqlalchemy.orm import declarative_base, relationship
from models.database import Base

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    instructorId = Column(Integer, ForeignKey("instructors.id"), nullable=False, index=True)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default=text('false'))
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    instructor = relationship("Instructor", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    schedules = relationship("CourseSchedule", back_populates="course", cascade="all, delete-orphan")
