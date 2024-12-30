from sqlmodel import SQLModel, Field, Relationship, Column, String
import uuid
from datetime import datetime, timezone
from typing import Optional
import enum


class Semesters(str, enum.Enum):
    FALL = 'FALL'
    SPRING = 'SPRING'


def get_utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(SQLModel, table=True):
    __tablename__ = 'users'  # type: ignore

    id: str = Field(
        primary_key=True,
        default_factory=lambda: str(uuid.uuid4()),
        index=True
    )

    username: str = Field(max_length=50, nullable=False, unique=True)
    password: str = Field(min_length=8, nullable=False)
    email: str = Field(max_length=50, nullable=False, unique=True)
    created_at: datetime = Field(
        default_factory=get_utc_now, nullable=False
    )
    userdata: Optional["UserData"] = Relationship(
        sa_relationship_kwargs={
            "back_populates": "user",
            "uselist": False,
            "cascade": "all, delete-orphan"
        }
    )

    def __repr__(self) -> str:
        return f"<User_{self.username}_{self.email}>"


class UserData(SQLModel, table=True):
    __tablename__ = 'user_data'  # type: ignore

    user_id: str = Field(
        foreign_key="users.id",
        primary_key=True
    )

    enrollment_semester: Semesters = Field(
        sa_column=Column(String, nullable=False)
    )
    graduation_semester: Semesters = Field(
        sa_column=Column(String, nullable=False)
    )

    enrollment_year: int = Field(nullable=False)
    graduation_year: int = Field(nullable=False)

    major: str = Field(nullable=False, max_length=20)
    minor: Optional[str] = Field(max_length=20)
    concentration: Optional[str] = Field(max_length=20)

    user: Optional[User] = Relationship(
        sa_relationship_kwargs={
            "back_populates": "userdata"
        }
    )

    def __repr__(self) -> str:
        return f"<UserData_{self.user_id}_{self.major}_{self.minor}_{self.concentration}>"
