import uuid
from datetime import date, datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserProfileBaseScheme(BaseModel):
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
    pass


class UserProfileUpdateScheme(UserProfileBaseScheme):
    pass


class UserProfileResponseScheme(UserProfileBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )


    model_config = ConfigDict(from_attributes=True)


