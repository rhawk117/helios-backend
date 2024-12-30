from sqlalchemy import Column, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from src.db.main import Base
import uuid
from typing import Optional


class UserData(Base):
    """[table=user_data]
    user-specific information; required to create a user 

    Attributes:
        id (str): UUID primary key for UserData.
        enrollment_date (Date): The date the user enrolled.
        graduation_date (Date): The expected graduation date.
        major (str): The user's major field of study.
        minor (Optional[str]): The user's minor field of study.
        concentration (Optional[str]): The user's academic concentration.
        user (User): Back-reference to the associated User instance.
    """
    __tablename__ = "user_data"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True
    )

    enrollment_date: Mapped[Date] = mapped_column(Date, nullable=False)
    graduation_date: Mapped[Date] = mapped_column(Date, nullable=False)

    major: Mapped[str] = mapped_column(String(100), nullable=False)
    minor: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    concentration: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="user_data",
        uselist=False
    )

    def __repr__(self):
        return (
            f"<UserData(id='{self.id}', major='{self.major}', "
            f"minor='{self.minor}', concentration='{self.concentration}')>"
        )


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (str): UUID primary key for the User.
        username (str): Unique username.
        password (str): Hashed user password.
        email (str): Unique user email.
        user_data_id (str): Foreign key reference to UserData.
        user_data (UserData): One-to-one relationship with UserData.
    """
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    user_data_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("user_data.id", ondelete="CASCADE"),
        unique=True,
        nullable=False
    )
    user_data: Mapped[UserData] = relationship(
        "UserData",
        back_populates="user_data",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return (
            f"<User(id='{self.id}', username='{self.username}', "
            f"email='{self.email}')>"
        )
