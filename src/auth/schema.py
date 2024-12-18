from pydantic import BaseModel, EmailStr, ConfigDict


class UserRegisterSchema(BaseModel):
    email: EmailStr
    phone_number: str
    password: str
    first_name: str


class UserLoginSchema(BaseModel):
    email: EmailStr | None = None
    phone_number: str | None = None
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    phone_number: str
    first_name: str
    last_name: str | None
    middle_name: str | None

    model_config = ConfigDict(from_attributes=True)


class CurrentUser(BaseModel):
    phone_number: str | None = None
    email: EmailStr | None = None
    