import uuid

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional


class ReviewBase(BaseModel):
    title: str = Field(..., max_length=255)
    stars: int = Field(..., ge=1, le=5)


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(ReviewBase):
    title: Optional[str] = Field(None, max_length=255)
    stars: Optional[int] = Field(None, ge=1, le=5)


class ReviewResponse(ReviewBase):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    model_config = ConfigDict(from_attributes=True)


class EmployerBase(BaseModel):
    title: str = Field(..., max_length=255)
    industry: str = Field(..., max_length=100)
    location: str = Field(..., max_length=100)


class EmployerCreate(EmployerBase):
    reviews: Optional[List[ReviewBase]] = None


class EmployerUpdate(EmployerBase):
    title: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    reviews: Optional[List[ReviewBase]] = None


class EmployerResponse(EmployerBase):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )
    reviews: List[ReviewResponse] = []

    model_config = ConfigDict(from_attributes=True)