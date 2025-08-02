from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Index, text
from sqlalchemy.orm import declarative_base, relationship
from models.database import Base

class Enrollment(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    studentId = Column(Integer, ForeignKey("students.id"), nullable=False)
    courseId = Column(Integer, ForeignKey("courses.id"), nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    __table_args__ = (
        Index("ix_enrollment_student_course", "studentId", "courseId", unique=True),
    )

