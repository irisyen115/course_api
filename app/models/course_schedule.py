from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time, text
from sqlalchemy.orm import declarative_base, relationship
from models.database import Base

class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    id = Column(Integer, primary_key=True, autoincrement=True)
    courseId = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    weekday = Column(Integer, nullable=False)
    startTime = Column(Time, nullable=False)
    endTime = Column(Time, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))

    course = relationship("Course", back_populates="schedules")

