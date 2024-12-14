from pydantic import BaseModel, EmailStr, Field


class UserRegisterSchema(BaseModel):
    email: EmailStr = Field(...)
    phone_number: str = Field(...)
    password: str = Field(...)
    first_name: str = Field(...)

class UserLoginSchema(BaseModel):
    phone_number: str | None = None
    email: EmailStr | None = None
    password: str = Field(...)

class GetUser(BaseModel):
    phone_number: str | None = None
    email: EmailStr | None = None
