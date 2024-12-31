from pydantic import BaseModel, EmailStr, Field, model_validator
from typing import Optional, Any


def no_whitespace(field: str, field_name: str) -> None:
    if ' ' in field:
        raise ValueError(f"{field_name} cannot contain whitespace.")


def check_pwd(password: str) -> None:
    '''
        checks password for:
        - whitespace
        - has digit
        - has lower & upper
    '''
    no_whitespace(password, "Password")
    if not any(char.isdigit() for char in password):
        raise ValueError("Password must contain at least one digit.")

    if not any(char.isalpha() for char in password):
        raise ValueError("Password must contain at least one letter.")

    if not any(char.isupper() for char in password):
        raise ValueError(
            "Password must contain at least one uppercase letter.")


class BaseUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    email: EmailStr = Field(..., max_length=100)

    @model_validator(mode='after')
    def validate_user_create(cls, model) -> Any:
        global no_whitespace, check_pwd
        if model.username:
            no_whitespace(model.username, "Username")
        if model.password:
            check_pwd(model.password)
        return model


class CreateUser(BaseUser):
    pass


class UserUpdate(BaseUser):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr


def main() -> None:
    try:
        base_user = CreateUser(
            username="user",
            password="Password1",
            email="test@yahoo.com"
        )
        print(base_user.model_dump())
    except ValueError as e:
        print(str(e))


if __name__ == '__main__':
    main()
