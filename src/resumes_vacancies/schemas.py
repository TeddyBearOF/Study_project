import uuid
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class VacancyBaseScheme(BaseModel):
    """Базовая схема вакансии"""
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
    """Схема для создания вакансии"""
    pass


class VacancyUpdateScheme(BaseModel):
    """Схема для обновления вакансии"""
    title: Optional[str] = Field(None, max_length=200)
    salary: Optional[int] = Field(None, ge=0)


class VacancyResponseScheme(VacancyBaseScheme):
    """Схема ответа с вакансией"""
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174000']
    )

    model_config = ConfigDict(from_attributes=True)


class ResumeBaseScheme(BaseModel):
    """Базовая схема резюме"""
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
    """Схема для создания резюме"""
    pass


class ResumeUpdateScheme(BaseModel):
    """Схема для обновления резюме"""
    candidate_name: Optional[str] = Field(None, max_length=100)
    main_skill: Optional[str] = Field(None, max_length=100)
    salary: Optional[int] = Field(None, ge=0)


class ResumeResponseScheme(ResumeBaseScheme):
    """Схема ответа с резюме"""
    id: uuid.UUID = Field(
        ...,
        examples=['123e4567-e89b-12d3-a456-426614174001']
    )
    vacancies_replied: List[VacancyResponseScheme] = []

    model_config = ConfigDict(from_attributes=True)


class VacancyWithResumesScheme(VacancyResponseScheme):
    """Схема вакансии с привязанными резюме"""
    resumes_replied: List[ResumeResponseScheme] = []


class ResumeWithVacanciesScheme(ResumeResponseScheme):
    """Схема резюме с привязанными вакансиями"""
    vacancies_replied: List[VacancyResponseScheme] = []


