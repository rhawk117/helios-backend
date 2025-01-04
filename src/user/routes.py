from typing import List

from fastapi import Depends, HTTPException, status, APIRouter, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.main import get_db
from src.models import User
from .schemas.user import (
    CreateUser,
    UserRead,
    UserUpdate,
    DemoCreateUser
)
from src.user.service import UserService

user_router = APIRouter(prefix="/user", tags=["user"])
user_service = UserService()

@user_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    create_user_schema: CreateUser,
    db: AsyncSession = Depends(get_db)
) -> UserRead:
    if await user_service.username_exists(db, create_user_schema):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists."
        )

    if await user_service.email_exists(db, create_user_schema):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists."
        )

    user = await user_service.create_user(db, create_user_schema)
    return user


@user_router.get("/all", response_model=List[UserRead], status_code=status.HTTP_200_OK)
async def get_all_users(db: AsyncSession = Depends(get_db)) -> List[UserRead]:
    users = await user_service.get_all(db)
    return users

# v---------[PATH PARAM ROUTES]---------v


@user_router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, db: AsyncSession = Depends(get_db)) -> None:
    deleted_user = await user_service.get_by(User.id == user_id, db)
    if not deleted_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    await user_service.delete_model(db, deleted_user)


@user_router.get("/{user_id}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)) -> UserRead:
    '''gets a user given an ID; 404 if not found'''
    user = await user_service.get_by(User.id == user_id, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    return user


@user_router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_user(
    user_update_schema: UserUpdate,
    user_id: str,
    db: AsyncSession = Depends(get_db)
) -> dict:

    user = await user_service.get_by(User.id == user_id, db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    user = await user_service.update_user(db, user, user_update_schema)
    return {"message": "User updated successfully."}
