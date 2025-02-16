from pydantic import BaseModel, Field

POSTFIX = "of student"

class FullStudent(BaseModel):
    id: int = Field(description=f"ID {POSTFIX}")
    name: str = Field(description=f"Name {POSTFIX}")
    age: int = Field(description=f"Age {POSTFIX}")
    email: str = Field(description=f"Email {POSTFIX}")
    courses: list[str | None] = Field(description="Courses in which the student participates")
