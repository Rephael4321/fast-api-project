from models.PydanticModels import StudentIn, StudentOut, StudentDB
from Querier import Querier

class StudentManager:
    def __init__(self) -> None:
        self.querier = Querier()

    async def getAllStudents(self) -> list[StudentDB]:
        """Retrieve all students."""

        result = await self.querier.getAllStudents()
        return [StudentDB(**row) for row in result]

    async def getStudentById(self, student_id: int) -> StudentDB:
        """Retrieve student by its ID"""

        result = await self.querier.getStudentById(student_id)
        if not result:
            raise KeyError
        return StudentDB(**result)

    async def addStudent(self, new_student: StudentIn) -> StudentOut:
        """Add a new student"""

        result = await self.querier.addStudent(new_student=new_student)
        return StudentOut(**result)

    async def updateStudent(self, student_id: int, updated_student: StudentIn) -> StudentOut:
        """Update a student by ID"""
        
        if all(getattr(updated_student, field) is None for field in updated_student.model_fields_set):
            raise ValueError
        result = await self.querier.updateStudent(student_id, updated_student)
        if not result:
            raise KeyError
        return StudentOut(**result)

    async def deleteStudent(self, student_id: int) -> StudentOut:
        """Delete a student by ID"""

        result = await self.querier.deleteStudent(student_id)
        if not result:
            raise KeyError
        return StudentOut(**result)
