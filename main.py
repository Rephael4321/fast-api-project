import asyncio
import uvicorn
from fastapi import FastAPI, HTTPException, Path
from StudentManager import StudentManager
from models.Student import Student
from models.StudentInput import StudentInput
from models.FullStudent import FullStudent
from Config import API_PORT

manager = StudentManager()

app = FastAPI(
    title="College Project",
    description="College Project served by rephael4321",
    version="1.0.0"
)

@app.get("/test_async")
async def asyncEndpoint():
    """Sleepy endpoint."""
    await asyncio.sleep(5)
    return {"message": "Response after 5 seconds"}

@app.get(path="/students")
def getStudents() -> list[FullStudent]:
    """Retrieve all students."""
    students = manager.getAllStudents()
    return students

@app.get(
        path="/students/{student_id}",
        responses={
            404: {"description": "Student not found."}
            }
        )
def getStudentById(
    student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    )) -> FullStudent:
    """Retrieve student by its ID"""
    try:
        student = manager.getStudentById(student_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id=} not found."
        )
    return student

@app.post("/students")
def addStudent(new_student: StudentInput) -> Student:
    """Add a new student"""
    student = manager.addStudent(new_student)
    return student

@app.put(
        path="/students/{student_id}",
        responses={
            404: {"description": "Item not found"},
            400: {"description": "No arguments specified"}
            }
        )
def updateStudent(
    updated_student: StudentInput,
    student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    )
    ) -> Student:
    """Update a student by ID"""
    try:
        student = manager.updateStudent(student_id, updated_student)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id=} not found."
        )
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=f"No parameters provided for update."
        )
    return student

@app.delete(
        path="/students/{student_id}",
        responses={
            404: {"description": "Student not found."}
            }
        )
def deleteStudent(student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    )) -> Student:
    """Delete a student by ID"""
    try:
        student = manager.deleteStudent(student_id)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Student with {student_id=} does not exist."
        )
    return student

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
