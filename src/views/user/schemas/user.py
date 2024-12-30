# src/schemas/user.py

from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional
from .user_data import (
    UserDataCreate,
    UserDataUpdate,
    UserDataResponse
)


class UserValidate:

    @staticmethod
    def no_whitespace(field: str, field_name: str) -> None:
        if ' ' in field:
            raise ValueError(f"{field_name} cannot contain whitespace.")

    @staticmethod
    def check_pwd(password: str) -> None:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        UserValidate.no_whitespace(password, "Password")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit.")

        if not any(char.isalpha() for char in password):
            raise ValueError("Password must contain at least one letter.")

        if not any(char.isupper() for char in password):
            raise ValueError(
                "Password must contain at least one uppercase letter.")


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    email: EmailStr = Field(..., max_length=100)
    user_data: UserDataCreate = Field(...)

    @model_validator(mode='after')
    def validate_user_create(cls, model):
        UserValidate.no_whitespace(model.username, "Username")
        UserValidate.check_pwd(model.password)
        return model


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)

    @model_validator(mode='after')
    def validate_user_update(cls, model):
        if model.username:
            UserValidate.no_whitespace(model.username, "Username")
        if model.password:
            UserValidate.check_pwd(model.password)
        return model


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    user_data: UserDataResponse

    class Config:
        orm_mode = True
