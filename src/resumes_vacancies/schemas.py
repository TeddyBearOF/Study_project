import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


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


class VacancyUpdateScheme(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    salary: Optional[int] = Field(None, ge=0)


class VacancyResponseScheme(VacancyBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    model_config = ConfigDict(from_attributes=True)


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


class ResumeUpdateScheme(BaseModel):
    candidate_name: Optional[str] = Field(None, max_length=100)
    main_skill: Optional[str] = Field(None, max_length=100)
    salary: Optional[int] = Field(None, ge=0)


class ResumeResponseScheme(ResumeBaseScheme):
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174001']
    )
    vacancies_replied: List['VacancyResponseScheme'] = []

    model_config = ConfigDict(from_attributes=True)


class VacancyWithResumesScheme(VacancyResponseScheme):
    resumes_replied: List['ResumeResponseScheme'] = []

    model_config = ConfigDict(from_attributes=True)


class ResumeWithVacanciesScheme(ResumeResponseScheme):
    vacancies_replied: List['VacancyResponseScheme'] = []

    model_config = ConfigDict(from_attributes=True)


ResumeResponseScheme.model_rebuild()
VacancyResponseScheme.model_rebuild()


