import uuid
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.models.user import User
from src.models.user_profile import UserProfile
from src.schemas.base_schemas import UserCreate, UserUpdate, UserProfileCreate, UserProfileUpdate


class UserService:

    @staticmethod
    async def create_user_with_profile(db: Session, user_data, profile_data):
        db_user = User(**user_data.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        profile_dict = profile_data.model_dump()
        profile_dict['user_id'] = db_user.id
        db_profile = UserProfile(**profile_dict)
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)

        result = db_user.__dict__
        result['user_profile'] = db_profile
        return result

    @staticmethod
    async def get_user_with_profile(db: Session, user_id: uuid.UUID):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user_data = user.__dict__
        user_data['user_profile'] = user.user_profile
        return user_data

    @staticmethod
    async def update_user_with_profile(db: Session, user_id: uuid.UUID, user_update_data, profile_update_data):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        for field, value in user_update_data.model_dump().items():
            setattr(db_user, field, value)

        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if db_profile:
            for field, value in profile_update_data.model_dump().items():
                setattr(db_profile, field, value)
        else:
            profile_dict = profile_update_data.model_dump()
            profile_dict['user_id'] = user_id
            db_profile = UserProfile(**profile_dict)
            db.add(db_profile)

        db.commit()
        db.refresh(db_user)
        db.refresh(db_profile)

        user_data = db_user.__dict__
        user_data['user_profile'] = db_profile
        return user_data

    @staticmethod
    async def delete_user_with_profile(db: Session, user_id: uuid.UUID):
        db_user = db.query(User).filter(User.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if db_profile:
            db.delete(db_profile)

        db.delete(db_user)
        db.commit()

        return {'message': "User and profile deleted successfully"}


class UserProfileService:

    @staticmethod
    async def get_user_profile(db: Session, user_id: uuid.UUID):
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        return profile

    @staticmethod
    async def update_user_profile(db: Session, user_id: uuid.UUID, profile_update_data):
        db_profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not db_profile:
            raise HTTPException(status_code=404, detail="User profile not found")

        for field, value in profile_update_data.model_dump().items():
            setattr(db_profile, field, value)

        db.commit()
        db.refresh(db_profile)
        return db_profile