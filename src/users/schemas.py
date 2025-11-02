import uuid
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    title: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    pass

    class Config:
        from_attributes = True



class UserProfileBase(BaseModel):
    title: str
    bio: str
    user_id: uuid.UUID


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    pass

    class Config:
        from_attributes = True



class UserWithProfile(User):
    user_profile: Optional[UserProfile] = None


class UserProfileWithUser(UserProfile):
    user: Optional[User] = None


class UserCreateWithProfile(BaseModel):
    user: UserCreate
    user_profile: UserProfileCreate


class UserUpdateWithProfile(BaseModel):
    user: UserUpdate
    user_profile: UserProfileUpdate


