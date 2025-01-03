from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict
from typing import Optional, Any
import enum

class Permissions(enum.Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

class ERRORS:
    DIGIT = "Password must contain at least one digit."
    LETTER = "Password must contain at least one letter."
    LOWER = "Password must contain at least one lowercase letter."
    UPPER = "Password must contain at least one uppercase letter."


class ValidateUser:

    @staticmethod
    def no_whitespace(field: str, field_name: str) -> None:
        assert not ' ' in field, f"{field_name} cannot have spaces."

    @staticmethod
    def check_pwd(password) -> None:
        '''
            checks password for:
            - whitespace
            - has digit
            - has lower & upper
        '''
        ValidateUser.no_whitespace(password, "Password")
        assert any(char.isdigit() for char in password), ERRORS.DIGIT
        assert any(char.isalpha() for char in password), ERRORS.LETTER
        assert any(char.islower() for char in password), ERRORS.LOWER
        assert any(char.isupper() for char in password), ERRORS.UPPER


class BaseUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8, max_length=255)
    email: EmailStr = Field(..., max_length=100)
    permission: Permissions = Permissions.user

    @model_validator(mode='after')
    def validate_user_create(cls, model) -> Any:
        global no_whitespace, check_pwd
        if model.username:
            ValidateUser.no_whitespace(model.username, "Username")
        if model.password:
            ValidateUser.check_pwd(model.password)
        return model


class CreateUser(BaseUser):
    pass    


class CreateAdmin(BaseUser):
    permission: Permissions = Permissions.admin


class UserUpdate(BaseUser):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=100)


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    permission: Permissions
    model_config = ConfigDict(from_attributes=True)


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
