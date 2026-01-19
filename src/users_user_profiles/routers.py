from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.db import get_session
from src.users_user_profiles.services import UserService
from src.users_user_profiles.schemas import (
    UserCreateScheme,
    UserResponseScheme,
    UserUpdateScheme
)

router = APIRouter(prefix="/users_user_profiles", tags=["users_user_profiles"])


@router.post(
    "/",
    response_model=UserResponseScheme,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    user_data: UserCreateScheme,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.create_user(session, user_data)


@router.get("/{user_id}", response_model=UserResponseScheme)
async def get_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.get_user_by_id(session, user_id)


@router.put("/{user_id}", response_model=UserResponseScheme)
async def update_user(
    user_id: uuid.UUID,
    user_data: UserUpdateScheme,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.update_user(session, user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    await UserService.delete_user(session, user_id)