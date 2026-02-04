import uuid
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from src.employers_reviews.reviews.schemas import ReviewBase, ReviewResponse


class EmployerBase(BaseModel):
    title: str = Field(..., max_length=255)
    industry: str = Field(..., max_length=100)
    location: str = Field(..., max_length=100)


class EmployerCreate(EmployerBase):
    reviews: Optional[List["ReviewBase"]] = None


class EmployerUpdate(EmployerBase):
    title: Optional[str] = Field(None, max_length=255)
    industry: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=100)
    reviews: Optional[List["ReviewBase"]] = None


class EmployerResponse(EmployerBase):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )
    reviews: List["ReviewResponse"] = []

    model_config = ConfigDict(from_attributes=True)


EmployerCreate.model_rebuild()
EmployerUpdate.model_rebuild()
EmployerResponse.model_rebuild()