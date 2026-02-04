from typing import List

from pydantic import ConfigDict

from src.resumes_vacancies.resumes.schemas import ResumeResponseScheme
from src.resumes_vacancies.vacancies.schemas import VacancyResponseScheme


class ResumeWithVacanciesScheme(ResumeResponseScheme):
    vacancies_replied: List["VacancyResponseScheme"] = []

    model_config = ConfigDict(from_attributes=True)


class VacancyWithResumesScheme(VacancyResponseScheme):
    resumes_replied: List['ResumeResponseScheme'] = []

    model_config = ConfigDict(from_attributes=True)


VacancyResponseScheme.model_rebuild()
ResumeResponseScheme.model_rebuild()