from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, DateTime, Boolean, text
from sqlalchemy.orm import declarative_base, relationship
from models.database import Base

class Instructor(Base):
    __tablename__ = "instructors"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    courses = relationship("Course", back_populates="instructor")
    created_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=text('CURRENT_TIMESTAMP'))
