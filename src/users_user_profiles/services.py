import uuid
from datetime import datetime, date
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.users_user_profiles.models import User, UserProfile
from src.users_user_profiles.schemas import UserCreateScheme, UserUpdateScheme


class UserService:
    @staticmethod
    async def create_user(
            session: AsyncSession,
            user_data: UserCreateScheme
    ) -> User:
        stmt = select(User).where(
            or_(User.username == user_data.username, User.email == user_data.email)
        )
        result = await session.execute(stmt)
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already exists"
            )

        user = User(
            username=user_data.username,
            email=user_data.email
        )
        session.add(user)
        await session.flush()

        if user_data.user_profile:
            profile_data = user_data.user_profile.model_dump()

            profile = UserProfile(
                user_id=user.id,
                **profile_data
            )
            session.add(profile)

        await session.commit()

        stmt = (
            select(User)
            .where(User.id == user.id)
            .options(selectinload(User.user_profile))
        )
        result = await session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def get_user_by_id(
            session: AsyncSession,
            user_id: uuid.UUID
    ) -> User:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(selectinload(User.user_profile))
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user


    @staticmethod
    async def update_user(
            session: AsyncSession,
            user_id: uuid.UUID,
            user_data: UserUpdateScheme
    ) -> User:
        user = await UserService.get_user_by_id(session, user_id)

        update_data = user_data.model_dump(exclude_unset=True, exclude={"user_profile"})
        for field, value in update_data.items():
            setattr(user, field, value)

        if user_data.user_profile:
            profile_data = user_data.user_profile.model_dump(exclude_unset=True)

            if not user.user_profile:
                profile = UserProfile(user_id=user.id, **profile_data)
                session.add(profile)
            else:
                for field, value in profile_data.items():
                    setattr(user.user_profile, field, value)

        await session.commit()
        await session.refresh(user)
        return user

    @staticmethod
    async def delete_user(
            session: AsyncSession,
            user_id: uuid.UUID
    ) -> bool:
        user = await UserService.get_user_by_id(session, user_id)

        await session.delete(user)
        await session.commit()

        return True