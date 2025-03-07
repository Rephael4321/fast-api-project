from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.sql.selectable import Select
from sqlalchemy.future import select
from sqlalchemy import func, insert, update, delete
from models.ORMModels import Student, Course, Enrollment
from models.PydanticModels import StudentIn
from Config import DB_URL

class Querier:
    def __init__(self):
        self.engine = create_async_engine(DB_URL)
        self.session_local = async_sessionmaker(bind=self.engine, expire_on_commit=False)

    def _buildGetAllStudentsQuery(self) -> Select:
        query = (
            select(
                Student.id,
                Student.name,
                Student.age,
                Student.email,
            ).outerjoin(
                Enrollment,
                Enrollment.student_id == Student.id
            ).outerjoin(
                Course,
                Enrollment.course_id == Course.id
            )
        )
        return query

    def _buildGroupResultQuery(self, origin_query: Select) -> Select:
        query = origin_query.group_by(
                    Student.id,
                    Student.name,
                    Student.age,
                    Student.email,
                ).add_columns(
                    func.json_agg(Course.name).label("courses")
                )
        return query

    async def getAllStudents(self) -> list[dict]:
        async with self.session_local() as session:
            get_all_students_query = self._buildGetAllStudentsQuery()
            group_result_query = self._buildGroupResultQuery(get_all_students_query)
            query_result = await session.execute(group_result_query)
            students = [row._asdict() for row in query_result]
        return students

    async def getStudentById(self, student_id: int) -> dict:
        async with self.session_local() as session:
            get_all_students_query = self._buildGetAllStudentsQuery()
            filter_students = get_all_students_query.where(Student.id == student_id)
            group_result_query = self._buildGroupResultQuery(filter_students)
            query_result = await session.execute(group_result_query)
            students = [row._asdict() for row in query_result]
        return students[0] if students else students

    async def addStudent(self, new_student: StudentIn) -> dict:
        async with self.session_local() as session:
            query = insert(
                                Student
                            ).values(
                                new_student.model_dump(
                                exclude_unset=True
                            )).returning(
                                Student.id, Student.name, Student.age, Student.email
                            )
            result = await session.execute(query)
            await session.commit()
            student = result.fetchone()._asdict()
            return student

    async def updateStudent(self, student_id: int, updated_student: StudentIn) -> dict:
        async with self.session_local() as session:
            query = (
                update(Student).where(
                    Student.id == student_id
                ).values(
                    updated_student.model_dump(exclude_unset=True)
                ).returning(
                    Student.id,
                    Student.name,
                    Student.age,
                    Student.email
                )
            )
            result = await session.execute(query)
            await session.commit()
            student = result.fetchone()
        return student._asdict() if student else {}

    async def deleteStudent(self, student_id: int) -> dict:
        async with self.session_local() as session:
            query = (
                delete(
                    Student
                ).where(
                    Student.id == student_id
                ).returning(
                    Student.id,
                    Student.name,
                    Student.age,
                    Student.email
                )
            )
            result = await session.execute(query)
            await session.commit()
            student = result.fetchone()
        return student._asdict() if student else {}
