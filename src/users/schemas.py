import uuid
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserProfileBaseScheme(BaseModel):
    """Базовая схема профиля"""
    full_name: Optional[str] = Field(
        None,
        max_length=100,
        examples=['Иван Иванов']
    )
    bio: Optional[str] = Field(
        None,
        max_length=500,
        examples=['Разработчик энвелоупов']
    )

    date_of_birth: Optional[date] = Field(
        None,
        examples=['1990-01-01']
    )


class UserProfileCreateScheme(UserProfileBaseScheme):
    """Схема для создания профиля"""
    pass


class UserProfileUpdateScheme(UserProfileBaseScheme):
    """Схема для обновления профиля"""
    pass


class UserProfileResponseScheme(UserProfileBaseScheme):
    """Схема ответа с профилем"""
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )


    model_config = ConfigDict(from_attributes=True)


class UserBaseScheme(BaseModel):
    username: str = Field(
        ...,
        min_length=2,
        max_length=30,
        pattern='^[a-zA-Z0-9_]+$',
        examples=['rudik_prudik']
    )

    email: EmailStr = Field(
        ...,
        examples=['user@example.com']
    )


class UserCreateScheme(UserBaseScheme):
    """Схема для создания пользователя"""
    user_profile: Optional[UserProfileCreateScheme] = None


class UserUpdateScheme(BaseModel):
    """Схема для обновления пользователя"""
    username: Optional[str] = Field(
        None,
        min_length=3,
        max_length=50,
        pattern='^[a-zA-Z0-9_]+$'
    )
    email: Optional[EmailStr] = None
    user_profile: Optional[UserProfileUpdateScheme] = None


class UserResponseScheme(UserBaseScheme):
    """Схема ответа с пользователем"""
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    user_profile: Optional[UserProfileResponseScheme] = None

    model_config = ConfigDict(from_attributes=True)


