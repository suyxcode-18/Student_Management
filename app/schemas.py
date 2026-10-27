
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class StudentBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=1, le=120)
    email: EmailStr
    course: str = Field(min_length=1, max_length=100)


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
