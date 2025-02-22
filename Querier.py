from sqlalchemy import create_engine, func, insert, update, delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from models.ORMModels import Student, Course, Enrollment
from models.PydanticModels import StudentIn
from Config import DB_URL
class Querier:
    def __init__(self):
        self.engine = create_engine(DB_URL)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def _queryAllStudents(self, session: Session) -> Query:
        query = (
            session.query(
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
        return [row._asdict() for row in query]

    def getAllStudents(self) -> list[dict]:
        with self.SessionLocal() as session:
            result = self._groupResult(self._queryAllStudents(session))
        return result

    def getStudentById(self, student_id: int) -> list[dict]:
        with self.SessionLocal() as session:
            student = self._groupResult(self._queryAllStudents(session).filter(Student.id == student_id))
        return student[0] if student else student

    def addStudent(self, new_student: StudentIn) -> dict:
        with self.SessionLocal() as session:
            stmt = insert(Student).values(new_student.model_dump(exclude_unset=True))
            result = session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
            session.commit()
        return result.fetchone()._asdict()

    def updateStudent(self, student_id: int, updated_student: StudentIn) -> dict:
        with self.SessionLocal() as session:
            stmt = update(Student).where(Student.id == student_id).values(updated_student.model_dump(exclude_unset=True))
            result = session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
            session.commit()
            student = result.fetchone()
        return student._asdict() if student else {}

    def deleteStudent(self, student_id: int) -> dict:
        with self.SessionLocal() as session:
            stmt = delete(Student).where(Student.id == student_id)
            result = session.execute(stmt.returning(Student.id, Student.name, Student.age, Student.email))
            session.commit()
            student = result.fetchone()
        return student._asdict() if student else {}
