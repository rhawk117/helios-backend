from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, desc
from src.views.user.schemas import UserCreate, UserUpdate, UserDataUpdate
from src.db.models.user import User, UserData
from src.utils.security import PasswordUtils
from src.config.logging import logger
from typing import Sequence, Optional


class UserService:
    '''user CRUD operations'''

    async def get_all_users(self, session: AsyncSession) -> Sequence[User]:
        statement = select(User).order_by(desc(User.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_user(self, session: AsyncSession, user_id: str) -> Optional[User]:
        statement = select(User).where(User.id == user_id)
        result = await session.exec(statement)
        return result.first()

    async def email_exists(self, session: AsyncSession, email: str) -> bool:
        statement = select(User).where(User.email == email)
        result = await session.exec(statement)
        return result.first() is not None

    async def username_exists(self, session: AsyncSession, username: str) -> bool:
        statement = select(User).where(User.username == username)
        result = await session.exec(statement)
        return result.first() is not None

    async def can_user_register(self, session: AsyncSession, user: dict) -> tuple[bool, str]:
        if await self.email_exists(session, user['email']):
            return (False, "Email already taken")

        if await self.username_exists(session, user['username']):
            return (False, "Username already taken")

        return (True, "User can register")

    async def create_user(self, session: AsyncSession, user_create_data: UserCreate) -> dict:
        logger.info(f"Creating new user: {user_create_data.username}")

        valid, message = await self.can_user_register(session, user_create_data.model_dump())
        if not valid:
            return {"error": message}

        hashed_password = PasswordUtils.hash_password(
            user_create_data.password)
        new_user = User(
            username=user_create_data.username,
            email=user_create_data.email,
            password=hashed_password
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        userdata = user_create_data.userdata
        if not userdata:
            logger.error("UserData is required to create a user")
            return {"error": "UserData is required to create a user"}

        new_userdata = UserData(
            user_id=new_user.id,
            enrollment_semester=userdata.enrollment_semester,  # type: ignore
            graduation_semester=userdata.graduation_semester,  # type: ignore
            enrollment_year=userdata.enrollment_year,
            graduation_year=userdata.graduation_year,
            major=userdata.major,
            minor=userdata.minor,
            concentration=userdata.concentration
        )
        session.add(new_userdata)
        await session.commit()
        await session.refresh(new_userdata)

        logger.info(
            f"User {new_user.username} created successfully with UserData."
        )
        return {"user": new_user, "userdata": new_userdata}

    async def update_user_data(
        self,
        userdata: UserData,
        userdata_update: UserDataUpdate
    ) -> UserData:
        for key, value in userdata_update.model_dump(exclude_unset=True).items():
            setattr(userdata, key, value)
        return userdata

    async def update_user(
        self,
        session: AsyncSession,
        user_id: str,
        user_data: UserUpdate
    ) -> dict:
        logger.debug(f"Updating user with ID: {user_id}")

        user = await self.get_user(session, user_id)
        if not user:
            logger.debug(f"User with ID {user_id} not found")
            return {"error": "User not found"}

        user_update = user_data.model_dump(exclude_unset=True)
        for key, value in user_update.items():
            if key == "password":
                user.password = PasswordUtils.hash_password(value)
            elif key == "userdata" and user_data.userdata and user.userdata:
                await self.update_user_data(user.userdata, user_data.userdata)
            else:
                setattr(user, key, value)

        await session.commit()
        await session.refresh(user)
        logger.debug(f"User with ID {user_id} updated successfully.")
        return {"user": user}

    async def delete_user(self, session: AsyncSession, user_id: str) -> dict:
        logger.debug(f"Deleting user with ID: {user_id}")

        user = await self.get_user(session, user_id)
        if not user:
            logger.debug(f"User with ID {user_id} not found")
            return {"error": "User not found"}

        await session.delete(user)
        await session.commit()
        logger.warning(f"User with ID {user_id} deleted successfully.")
        return {"message": "User deleted successfully"}
