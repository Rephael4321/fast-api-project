from pydantic import BaseModel, Field
from app.Config import POSTFIX

class StudentIn(BaseModel):
    name: str | None = Field(description=f"Name {POSTFIX}")
    age: int | None = Field(description=f"Age {POSTFIX}")
    email: str | None = Field(description=f"Email {POSTFIX}")

class StudentOut(StudentIn):
    id: int = Field(description=f"ID {POSTFIX}")

class StudentDB(StudentOut):
    courses: list[str | None] = Field(description="Courses in which the student participates")
