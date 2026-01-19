from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from src.db import get_session
from src.resumes_vacancies.services import (
    ResumeService, VacancyService
)
from src.resumes_vacancies.schemas import (
    ResumeCreateScheme, ResumeResponseScheme, ResumeUpdateScheme,
    VacancyCreateScheme, VacancyResponseScheme, VacancyUpdateScheme,
    ResumeWithVacanciesScheme, VacancyWithResumesScheme
)

router = APIRouter(prefix="/resumes-vacancies", tags=["resumes-vacancies"])


@router.post(
    "/resumes/",
    response_model=ResumeResponseScheme,
    status_code=status.HTTP_201_CREATED
)
async def create_resume(
    resume_data: ResumeCreateScheme,
    session: AsyncSession = Depends(get_session)
):
    return await ResumeService.create_resume(session, resume_data)


@router.get("/resumes/{resume_id}", response_model=ResumeResponseScheme)
async def get_resume(
        resume_id: uuid.UUID,
        with_vacancies: bool = Query(False, description="Включить связанные вакансии"),
        session: AsyncSession = Depends(get_session)
):
    resume = await ResumeService.get_resume_by_id(
        session, resume_id, with_vacancies=with_vacancies
    )

    if with_vacancies:
        return ResumeWithVacanciesScheme.from_orm(resume)
    else:
        return ResumeResponseScheme.from_orm(resume)


@router.get("/resumes/", response_model=list[ResumeResponseScheme])
async def get_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session)
):
    return await ResumeService.get_resumes(session, skip, limit)


@router.put("/resumes/{resume_id}", response_model=ResumeResponseScheme)
async def update_resume(
        resume_id: uuid.UUID,
        resume_data: ResumeUpdateScheme,
        session: AsyncSession = Depends(get_session)
):
    return await ResumeService.update_resume(session, resume_id, resume_data)


@router.delete(
    "/resumes/{resume_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_resume(
        resume_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    await ResumeService.delete_resume(session, resume_id)


@router.post(
    "/vacancies/",
    response_model=VacancyResponseScheme,
    status_code=status.HTTP_201_CREATED
)
async def create_vacancy(
        vacancy_data: VacancyCreateScheme,
        session: AsyncSession = Depends(get_session)
):
    return await VacancyService.create_vacancy(session, vacancy_data)


@router.get("/vacancies/{vacancy_id}", response_model=VacancyResponseScheme)
async def get_vacancy(
        vacancy_id: uuid.UUID,
        with_resumes: bool = Query(False, description="Включить связанные резюме"),
        session: AsyncSession = Depends(get_session)
):
    vacancy = await VacancyService.get_vacancy_by_id(
        session, vacancy_id, with_resumes=with_resumes
    )

    if with_resumes:
        return VacancyWithResumesScheme.from_orm(vacancy)
    else:
        return VacancyResponseScheme.from_orm(vacancy)


@router.get("/vacancies/", response_model=list[VacancyResponseScheme])
async def get_vacancies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    session: AsyncSession = Depends(get_session)
):
    return await VacancyService.get_vacancies(session, skip, limit)


@router.put("/vacancies/{vacancy_id}", response_model=VacancyResponseScheme)
async def update_vacancy(
        vacancy_id: uuid.UUID,
        vacancy_data: VacancyUpdateScheme,
        session: AsyncSession = Depends(get_session)
):
    return await VacancyService.update_vacancy(session, vacancy_id, vacancy_data)


@router.delete(
    "/vacancies/{vacancy_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_vacancy(
        vacancy_id: uuid.UUID,
        session: AsyncSession = Depends(get_session)
):
    await VacancyService.delete_vacancy(session, vacancy_id)