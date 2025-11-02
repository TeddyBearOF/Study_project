from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid as uuid

from src.db import get_session
from src.users.schemas import UserWithProfile, UserCreateWithProfile, User, UserProfile, UserUpdateWithProfile

router = APIRouter(prefix="/users", tags=["users"])



@router.post("/", response_model=UserWithProfile)
async def create_user_with_profile(
        user_data: UserCreateWithProfile,
        session: Session = Depends(get_session)
):
    #model_dump
    db_user = User(**user_data.user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    profile_data = user_data.user_profile.dict()
    profile_data['user_id'] = db_user.id
    db_profile = UserProfile(**profile_data)
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)

    result = db_user.__dict__
    result['user_profile'] = db_profile
    return result


@router.get("/{user_id}", response_model=UserWithProfile)
async def read_user(
        user_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_data = user.__dict__
    user_data['user_profile'] = user.user_profile
    return user_data


@router.put("/{user_id}", response_model=UserWithProfile)
async def update_user_with_profile(  # ✅ async
        user_id: uuid.UUID,
        user_data: UserUpdateWithProfile,
        session: Session = Depends(get_session)
):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_data.user.dict().items():
        setattr(db_user, field, value)

    db_profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if db_profile:
        for field, value in user_data.user_profile.dict().items():
            setattr(db_profile, field, value)
    else:
        profile_data = user_data.user_profile.dict()
        profile_data['user_id'] = user_id
        db_profile = UserProfile(**profile_data)
        session.add(db_profile)

    session.commit()
    session.refresh(db_user)
    session.refresh(db_profile)

    user_data = db_user.__dict__
    user_data['user_profile'] = db_profile
    return user_data


@router.delete("/{user_id}")
async def delete_user(
        user_id: uuid.UUID,
        session: Session = Depends(get_session)
):
    db_user = session.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_profile = session.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if db_profile:
        session.delete(db_profile)

    session.delete(db_user)
    session.commit()

    return {"message": "User and profile deleted successfully"}