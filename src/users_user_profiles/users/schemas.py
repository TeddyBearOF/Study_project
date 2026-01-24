import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from src.users_user_profiles.user_profiles.schemas import (
    UserProfileCreateScheme,
    UserProfileUpdateScheme,
    UserProfileResponseScheme,
)


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
    user_profile: Optional["UserProfileCreateScheme"] = None


class UserUpdateScheme(BaseModel):
    username: Optional[str] = Field(
        None,
        min_length=2,
        max_length=50,
        pattern='^[a-zA-Z0-9_]+$'
    )
    email: Optional[EmailStr] = None
    user_profile: Optional["UserProfileUpdateScheme"] = None


class UserResponseScheme(UserBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    user_profile: Optional["UserProfileResponseScheme"] = None

    model_config = ConfigDict(from_attributes=True)


UserCreateScheme.model_rebuild()
UserUpdateScheme.model_rebuild()
UserResponseScheme.model_rebuild()
