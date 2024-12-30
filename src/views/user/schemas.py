from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class UserValidators:
    @staticmethod
    def has_whitespace(value: str) -> None:
        '''raises if whitespace'''
        if ' ' in value:
            raise ValueError(
                "Both username and password cannot contain spaces!"
            )

    @staticmethod
    def check_password_requirements(password: str) -> None:
        if ' ' in password:
            raise ValueError("Password cannot contain spaces")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in password):
            raise ValueError(
                "Password must contain at least one uppercase letter")
        if not any(char.islower() for char in password):
            raise ValueError(
                "Password must contain at least one lowercase letter")
        UserValidators.has_whitespace(password)

    @staticmethod
    def check_dates(enrollment: int, graduation: int) -> None:
        if enrollment >= graduation:
            raise ValueError("Enrollment year cannot be after graduation year")


class SemesterEnum(str, Enum):
    FALL = 'FALL'
    SPRING = 'SPRING'


class UserDataBase(BaseModel):
    enrollment_semester: Optional[SemesterEnum] = None
    graduation_semester: Optional[SemesterEnum] = None
    enrollment_year: Optional[int] = Field(None, ge=2000, le=2100)
    graduation_year: Optional[int] = Field(None, ge=2000, le=2100)
    major: Optional[str] = Field(None, max_length=50)
    minor: Optional[str] = Field(None, max_length=50)
    concentration: Optional[str] = Field(None, max_length=50)


class UserDataCreate(UserDataBase):
    enrollment_semester: SemesterEnum = Field(nullable=False)  # type: ignore
    graduation_semester: SemesterEnum = Field(nullable=False)  # type: ignore
    enrollment_year: int = Field(ge=2000, le=2100)
    graduation_year: int = Field(ge=2000, le=2100)
    major: str = Field(max_length=50)

    @model_validator(mode='after')
    def validate_dates(cls, data):
        enrollment_year = data.enrollment_year
        graduation_year = data.graduation_year

        UserValidators.check_dates(enrollment_year, graduation_year)

        if enrollment_year > datetime.now().year:
            raise ValueError("Enrollment year cannot be in the future")
        if graduation_year < datetime.now().year:
            raise ValueError("Graduation year cannot be in the past")

        return data


class UserDataUpdate(UserDataBase):
    @model_validator(mode='after')
    def validate_dates(cls, data):
        enrollment_year = data.enrollment_year
        graduation_year = data.graduation_year

        if enrollment_year and graduation_year:
            UserValidators.check_dates(enrollment_year, graduation_year)
        return data


class UserBase(BaseModel):
    username: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None

    @field_validator("username")
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        if v:
            UserValidators.has_whitespace(v)
        return v


class UserCreate(UserBase):
    username: str = Field(max_length=50)
    email: EmailStr  # type: ignore
    password: str = Field(min_length=8)
    userdata: UserDataCreate

    @field_validator("password")
    def validate_password(cls, v: str) -> str:
        UserValidators.check_password_requirements(v)
        return v


class UserUpdate(UserBase):
    password: Optional[str] = Field(None, min_length=8)
    userdata: Optional[UserDataUpdate] = None

    @field_validator("password")
    def validate_password(cls, v: Optional[str]) -> Optional[str]:
        if v:
            UserValidators.check_password_requirements(v)
        return v


class UserResponse(UserBase):
    id: str
    created_at: datetime
    userdata: Optional[UserDataCreate]

    class Config:
        orm_mode = True
