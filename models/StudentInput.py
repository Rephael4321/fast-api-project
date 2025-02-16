from pydantic import BaseModel, Field

POSTFIX = "of student"

class StudentInput(BaseModel):
    name: str | None = Field(description=f"Name {POSTFIX}")
    age: int | None = Field(description=f"Age {POSTFIX}")
    email: str | None = Field(description=f"Email {POSTFIX}")
