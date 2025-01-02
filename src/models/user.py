import enum
import uuid
from sqlalchemy import String, Column, CheckConstraint
from src.db.main import Base


class Permissions(str, enum.Enum):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

class User(Base):
    """[table="users"]
    models the user info, one-to-one -> user_data

    Attributes:
        id (str): UUID primary key for the User.
        username (str): Unique username.
        password (str): Hashed user password.
        email (str): Unique user email.
        user_data_id (str): Foreign key reference to UserData.
        user_data (UserData): One-to-one relationship with UserData.
    """

    __tablename__ = "users"

    id = Column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        index=True
    )
    
    username = Column(
        String(50),
        unique=True,
        nullable=False
    )
    
    password = Column(String(255), nullable=False)

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )
    
    permission = Column(
        String(25),
        default=Permissions.user.value,
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            permission.in_([perm.value for perm in Permissions]),
            name="check_permission"
        ),   
    )


    
    # user_data: Mapped[UserData] = relationship(
    #     "UserData",
    #     back_populates="user_data",
    #     uselist=False,
    #     cascade="all, delete-orphan"
    # )

    def __repr__(self) -> str:
        return (
            f"<User(id='{self.id}', username='{self.username}', "
            f"email='{self.email}')>"
        )

