from sqlalchemy.ext.asyncio import AsyncSession
from src.db import CRUDService
from ..models.user import User
from .schemas import (
    CreateUser,
    UserUpdate,
    BaseUser
)
from fastapi import HTTPException, status
from src.utils.security import PasswordUtils


class UserService(CRUDService[User]):
    def __init__(self) -> None:
        super().__init__(User)

    async def username_exists(self, db: AsyncSession, user_schema_obj: BaseUser) -> bool:
        existing_username = await self.get_by(
            User.username == user_schema_obj.username,
            db,
        )
        return existing_username is not None

    async def email_exists(
        self,
        db: AsyncSession,
        user_schema_obj: BaseUser,
    ) -> bool:
        existing_email = await self.get_by(
            User.email == user_schema_obj.email,
            db,
        )
        return existing_email is not None

    async def hash_user_pwd(self, serialized_schema: dict) -> None:
        plain_pwd = serialized_schema.get('password')
        if not plain_pwd:
            raise ValueError("Password not provided.")
        serialized_schema['password'] = PasswordUtils.hash_password(plain_pwd)

    async def create_user(self, db: AsyncSession, create_user_schema: CreateUser) -> User:
        user_in = create_user_schema.model_dump()
        await self.hash_user_pwd(user_in)
        return await self.create(db, user_in)

    async def update_user(
        self,
        db: AsyncSession,
        user: User, 
        user_update_schema: UserUpdate
    ) -> None:
        
        user_data = user_update_schema.model_dump(exclude_unset=True)
        if user_data.get('password'):
            await self.hash_user_pwd(user_data)
        await self.update(db, user, user_data)

    async def delete_user(self, db: AsyncSession, user_id: str,) -> None:
        user = await self.get_by(User.id == user_id, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        await self.delete_model(db, user)

    async def check_credentials(
        self,
        db: AsyncSession,
        username: str,
        password: str
    ) -> bool:
        user_model = await self.get_by(User.username == username, db)
        if not user_model:
            return False

        return PasswordUtils.verify_password(
            password, user_model.password  # type: ignore
        )


user_mngr = UserService()


