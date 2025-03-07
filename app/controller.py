from fastapi import APIRouter, Depends, HTTPException, Path
from StudentManager import StudentManager
from models.PydanticModels import StudentIn, StudentOut, StudentDB

router = APIRouter()

@router.get(path="/students")
async def getStudents(manager: StudentManager = Depends()) -> list[StudentDB]:
    """Retrieve all students."""
    
    students = await manager.getAllStudents()
    return students

@router.get(
        path="/students/{student_id}",
        responses={
            404: {"description": "Student not found."}
            }
        )
async def getStudentById(
    student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    ),
    manager: StudentManager = Depends()) -> StudentDB:
    """Retrieve student by its ID"""
    
    try:
        student = await manager.getStudentById(student_id)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id=} not found."
        )
    return student

@router.post("/students")
async def addStudent(
    new_student: StudentIn,
    manager: StudentManager = Depends()) -> StudentOut:
    """Add a new student"""
    
    student = await manager.addStudent(new_student)
    return student

@router.put(
        path="/students/{student_id}",
        responses={
            404: {"description": "Item not found"},
            400: {"description": "No arguments specified"}
            }
        )
async def updateStudent(
    updated_student: StudentIn,
    student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    ),
    manager: StudentManager = Depends()) -> StudentOut:
    """Update a student by ID"""
    
    try:
        student = await manager.updateStudent(student_id, updated_student)
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

@router.delete(
        path="/students/{student_id}",
        responses={
            404: {"description": "Student not found."}
            }
        )
async def deleteStudent(student_id: int = Path(
        title="Student ID",
        description="Unique integer that specifies a student.",
        ge=0
    ),
    manager: StudentManager = Depends()) -> StudentOut:
    """Delete a student by ID"""
    
    try:
        student = await manager.deleteStudent(student_id)
    except KeyError:
        raise HTTPException(
            status_code=404, detail=f"Student with {student_id=} does not exist."
        )
    return student
