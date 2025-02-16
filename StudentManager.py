from models.Student import Student
from models.StudentInput import StudentInput
from models.FullStudent import FullStudent
import sqlalchemy
import Config
from queries import QUERIES

class StudentManager:
    def __init__(self) -> None:
        self.engine = sqlalchemy.create_engine(Config.DATABASE_URI)

    def getAllStudents(self) -> list[FullStudent]:
        """Retrieve all students."""

        with self.engine.connect() as connection:
            result = connection.execute(sqlalchemy.text(QUERIES["get_all_students_query"])).mappings()
        return [FullStudent(**row) for row in result]

    def getStudentById(self, student_id: int) -> FullStudent:
        """Retrieve student by its ID"""

        with self.engine.connect() as connection:
            result = connection.execute(
                                        sqlalchemy.text(QUERIES["get_student_by_id_query"]),
                                        {"student_id": student_id}
                                        ).mappings().fetchone()
        if result is None:
            raise KeyError
        student = FullStudent(**result)
        return student

    def addStudent(self, new_student: StudentInput) -> Student:
        """Add a new student"""

        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
                sqlalchemy.text(QUERIES["add_student_query"]),
                {**new_student.model_dump()}
                ).fetchone()[0]
            transaction.commit()
        student = Student(**result)
        return student

    def updateStudent(self, student_id: int, updated_student: StudentInput) -> Student:
        """Update a student by ID"""
        if all(getattr(updated_student, field) is None for field in updated_student.model_fields_set):
            raise ValueError
        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
                sqlalchemy.text(QUERIES["update_student_query"]),
                {"student_id": student_id, **updated_student.model_dump()}
                ).fetchone()
            transaction.commit()
        if result is None:
            raise KeyError
        student = Student(**result[0])
        return student

    def deleteStudent(self, student_id: int) -> Student:
        """Delete a student by ID"""

        with self.engine.connect() as connection:
            transaction = connection.begin()
            result = connection.execute(
                sqlalchemy.text(QUERIES["delete_student_query"]),
                {"student_id": student_id}
                ).fetchone()
            transaction.commit()
        if result is None:
            raise KeyError
        student = Student(**result[0])
        return student
