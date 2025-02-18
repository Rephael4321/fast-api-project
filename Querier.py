import sqlalchemy
from sqlalchemy import create_engine, func, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from models.ORMModels import Student, Course, Enrollment
from Config import DATABASE_URI
from models.PydanticModels import StudentIn

# TODO: FIX TYPES
class Querier:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def _queryAllStudents(self) -> Query:
        query = (
            self.session.query(
            Student.id,
            Student.name,
            Student.age,
            Student.email,
            func.json_agg(Course.name).label("courses")
        ).outerjoin(
            Enrollment,
            Enrollment.student_id == Student.id
            ).outerjoin(
                Course,
                Enrollment.course_id == Course.id
                )
        )
        return query

    def _groupResult(self, origin_query: Query) -> list[dict]:
        query = origin_query.group_by(
                    Student.id,
                    Student.name,
                    Student.age,
                    Student.email,
                ).all()
        self.session.close()
        return [row._asdict() for row in query]

    def getAllStudents(self) -> list[dict]:
        return self._groupResult(self._queryAllStudents())

    def getStudentById(self, student_id: int) -> list[dict]:
        student = self._groupResult(self._queryAllStudents().filter(Student.id == student_id))
        if student:
            return student[0]
        else:
            return student

    def addStudent(self, new_student: StudentIn) -> dict:
        stmt = insert(Student).values(new_student.model_dump(exclude_unset=True))
        result = self.session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
        self.session.commit()
        self.session.close()
        return result.fetchone()._asdict()

    def updateStudent(self, student_id: int, updated_student: StudentIn) -> dict:
        stmt = update(Student).where(Student.id == student_id).values(updated_student.model_dump(exclude_unset=True))
        result = self.session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
        self.session.commit()
        student = result.fetchone()
        self.session.close()
        if student:
            return student._asdict()
        else:
            return {}

    def deleteStudent(self, student_id: int) -> dict:
        stmt = delete(Student).where(Student.id == student_id)
        result = self.session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
        self.session.commit()
        student = result.fetchone()
        self.session.close()
        if student:
            return student._asdict()
        else:
            return {}
