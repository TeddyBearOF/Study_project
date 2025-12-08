from fastapi import APIRouter, Depends, HTTPException
import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_session
from src.users.services import UserService, UserProfileService
from src.schemas.composite_schemas import UserWithProfile, UserCreateWithProfile, UserUpdateWithProfile, UserProfile, \
    UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserWithProfile, status_code=201)
async def create_user_with_profile(
    user_data: UserCreateWithProfile,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.create_user_with_profile(
        session,
        user_data.user,
        user_data.user_profile
    )

@router.get("/{user_id}", response_model=UserWithProfile, status_code=200)
async def read_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.get_user_with_profile(session, user_id)

@router.put("/{user_id}", response_model=UserWithProfile, status_code=200)
async def update_user_with_profile(
    user_id: uuid.UUID,
    user_data: UserUpdateWithProfile,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.update_user_with_profile(
        session,
        user_id,
        user_data.user,
        user_data.user_profile
    )

@router.delete("/{user_id}", status_code=204)
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await UserService.delete_user_with_profile(session, user_id)

@router.get("/{user_id}/profile", response_model=UserProfile, status_code=200)
async def get_user_profile(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session)
):
    return await UserProfileService.get_user_profile(session, user_id)

@router.put("/{user_id}/profile", response_model=UserProfile, status_code=200)
async def update_user_profile(
    user_id: uuid.UUID,
    profile_data: UserProfileUpdate,
    session: AsyncSession = Depends(get_session)
):
    return await UserProfileService.update_user_profile(session, user_id, profile_data)
