import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import InvalidInputDataException
from src.resumes_vacancies.resumes.models import Resume


class VacancyBaseScheme(BaseModel):
    title: str = Field(
        ...,
        max_length=200,
        examples=['Middle Python Developer']
    )
    salary: Optional[int] = Field(
        None,
        ge=0,
        examples=[250000]
    )


class VacancyCreateScheme(VacancyBaseScheme):
    resumes_replied: List[uuid.UUID] = Field(default_factory=list)

    async def validate_resumes_replied(self, session: AsyncSession) -> None:
        if not self.resumes_replied:
            return

        stmt = select(Resume.id).where(Resume.id.in_(self.resumes_replied))
        result = await session.execute(stmt)
        existing_ids = {row[0] for row in result.fetchall()}
        invalid_ids = set(self.resumes_replied) - existing_ids

        if invalid_ids:
            raise InvalidInputDataException(
                f"Resumes not found: {sorted(list(invalid_ids))}"
            )



class VacancyUpdateScheme(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    salary: Optional[int] = Field(None, ge=0)


class VacancyResponseScheme(VacancyBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    model_config = ConfigDict(from_attributes=True)


