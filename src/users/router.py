from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid

from src.db import get_session
from src.users.services import UserService, UserProfileService
from src.schemas.composite_schemas import UserWithProfile, UserCreateWithProfile, UserUpdateWithProfile, UserProfile, \
    UserProfileUpdate

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserWithProfile)
async def create_user_with_profile(
    user_data: UserCreateWithProfile,
    session: Session = Depends(get_session)
):
    return await UserService.create_user_with_profile(
        session,
        user_data.user,
        user_data.user_profile
    )

@router.get("/{user_id}", response_model=UserWithProfile)
async def read_user(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await UserService.get_user_with_profile(session, user_id)

@router.put("/{user_id}", response_model=UserWithProfile)
async def update_user_with_profile(
    user_id: uuid.UUID,
    user_data: UserUpdateWithProfile,
    session: Session = Depends(get_session)
):
    return await UserService.update_user_with_profile(
        session,
        user_id,
        user_data.user,
        user_data.user_profile
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await UserService.delete_user_with_profile(session, user_id)

@router.get("/{user_id}/profile", response_model=UserProfile)
async def get_user_profile(
    user_id: uuid.UUID,
    session: Session = Depends(get_session)
):
    return await UserProfileService.get_user_profile(session, user_id)

@router.put("/{user_id}/profile", response_model=UserProfile)
async def update_user_profile(
    user_id: uuid.UUID,
    profile_data: UserProfileUpdate,
    session: Session = Depends(get_session)
):
    return await UserProfileService.update_user_profile(session, user_id, profile_data)