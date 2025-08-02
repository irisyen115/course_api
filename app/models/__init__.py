from .database import Base, engine
from .course import Course
from .instructor import Instructor
from .course_schedule import CourseSchedule
from .student import Student
from .enrollment import Enrollment

Base.metadata.create_all(bind=engine)