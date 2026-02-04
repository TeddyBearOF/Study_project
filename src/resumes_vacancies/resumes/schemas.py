import uuid
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import InvalidInputDataException
from src.resumes_vacancies.vacancies.models import Vacancy
from src.resumes_vacancies.vacancies.schemas import VacancyResponseScheme


class ResumeBaseScheme(BaseModel):
    candidate_name: str = Field(
        ...,
        max_length=100,
        examples=['Рудик Прудик']
    )
    main_skill: str = Field(
        ...,
        max_length=100,
        examples=['Python']
    )
    salary: Optional[int] = Field(
        None,
        ge=0,
        examples=[2000]
    )


class ResumeCreateScheme(ResumeBaseScheme):
    vacancies_replied: List[uuid.UUID] = Field(default_factory=list)

    async def validate_vacancies_replied(self, session: AsyncSession) -> None:
        if not self.vacancies_replied:
            return

        stmt = select(Vacancy.id).where(Vacancy.id.in_(self.vacancies_replied))
        result = await session.execute(stmt)
        existing_ids = {row[0] for row in result.fetchall()}
        invalid_ids = set(self.vacancies_replied) - existing_ids

        if invalid_ids:
            raise InvalidInputDataException(
                f"Vacancies not found: {sorted(list(invalid_ids))}"
            )


class ResumeUpdateScheme(BaseModel):
    candidate_name: Optional[str] = Field(None, max_length=100)
    main_skill: Optional[str] = Field(None, max_length=100)
    salary: Optional[int] = Field(None, ge=0)


class ResumeResponseScheme(ResumeBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174001']
    )
    vacancies_replied: List["VacancyResponseScheme"] = []

    model_config = ConfigDict(from_attributes=True)


ResumeResponseScheme.model_rebuild()


