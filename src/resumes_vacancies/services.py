import uuid
from typing import List, Optional, Any, Coroutine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload

from src.exceptions import EntityNotFoundException, InvalidInputDataException
from src.resumes_vacancies.models import VacancyResume
from src.resumes_vacancies.resumes.models import Resume
from src.resumes_vacancies.resumes.schemas import ResumeCreateScheme, ResumeUpdateScheme, ResumeResponseScheme
from src.resumes_vacancies.vacancies.models import Vacancy
from src.resumes_vacancies.vacancies.schemas import VacancyCreateScheme, VacancyUpdateScheme, VacancyResponseScheme


class ResumeService:
    @staticmethod
    async def create_resume(
            session: AsyncSession,
            resume_data: ResumeCreateScheme
    ) -> Resume:

        await resume_data.validate_vacancies_replied(session)

        resume = Resume(**resume_data.model_dump())
        session.add(resume)
        await session.flush()

        if resume_data.vacancies_replied:
            vacancies = await session.scalars(
                select(Vacancy).where(Vacancy.id.in_(resume_data.vacancies_replied))
            )
            resume.vacancies_replied.extend(vacancies)

        await session.commit()

        select_final_stmt = (
            select(Resume)
            .where(Resume.id == resume.id)
            .options(selectinload(Resume.vacancies_replied))
        )
        result = await session.execute(select_final_stmt)
        return result.scalar_one()

    @staticmethod
    async def get_resume_by_id(
            session: AsyncSession,
            resume_id: uuid.UUID,
            with_vacancies: bool = False
    ) -> Resume:
        stmt = select(Resume).where(Resume.id == resume_id)
        stmt = stmt.options(selectinload(Resume.vacancies_replied))
        result = await session.execute(stmt)
        resume = result.scalar_one_or_none()

        if not resume:
            raise EntityNotFoundException("Resume", str(resume_id))

        return resume

    @staticmethod
    async def get_resumes(
            session: AsyncSession,
            skip: int = 0,
            limit: int = 100
    ) -> List[Resume]:
        stmt = (
            select(Resume)
            .options(selectinload(Resume.vacancies_replied))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update_resume(
            session: AsyncSession,
            resume_id: uuid.UUID,
            resume_data: ResumeUpdateScheme
    ) -> Resume:
        resume = await ResumeService.get_resume_by_id(session, resume_id)

        update_data = resume_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resume, field, value)

        await session.commit()
        await session.refresh(resume)
        return resume


    @staticmethod
    async def delete_resume(
            session: AsyncSession,
            resume_id: uuid.UUID
    ) -> ResumeResponseScheme:
        resume = await ResumeService.get_resume_by_id(session, resume_id)
        await session.delete(resume)
        await session.commit()
        return ResumeResponseScheme.model_validate(resume)


class VacancyService:
    @staticmethod
    async def create_vacancy(
            session: AsyncSession,
            vacancy_data: VacancyCreateScheme
    ) -> Vacancy:

        await vacancy_data.validate_resumes_replied(session)

        vacancy = Vacancy(**vacancy_data.model_dump())
        session.add(vacancy)
        await session.flush()

        if vacancy_data.resumes_replied:
            result = await session.scalars(
                select(Resume).where(Resume.id.in_(vacancy_data.resumes_replied))
            )
            resumes = result.all()
            vacancy.resumes_replied.extend(resumes)

        await session.commit()

        select_final_stmt = (
            select(Vacancy)
            .where(Vacancy.id == vacancy.id)
            .options(selectinload(Vacancy.resumes_replied))
        )
        result = await session.execute(select_final_stmt)
        return result.scalar_one()

    @staticmethod
    async def get_vacancy_by_id(
            session: AsyncSession,
            vacancy_id: uuid.UUID,
            with_resumes: bool = False
    ) -> Vacancy:
        stmt = select(Vacancy)
        if with_resumes:
            stmt = stmt.options(selectinload(Vacancy.resumes_replied))
        stmt = stmt.where(Vacancy.id == vacancy_id)
        result = await session.execute(stmt)
        vacancy = result.scalar_one_or_none()

        if not vacancy:
            raise EntityNotFoundException("Vacancy", str(vacancy_id))

        return vacancy

    @staticmethod
    async def get_vacancies(
            session: AsyncSession,
            skip: int = 0,
            limit: int = 100
    ) -> List[Vacancy]:
        stmt = (
            select(Vacancy)
            .options(selectinload(Vacancy.resumes_replied))
            .offset(skip)
            .limit(limit)
        )
        result = await session.execute(stmt)
        return list(result.scalars().all())

    @staticmethod
    async def update_vacancy(
            session: AsyncSession,
            vacancy_id: uuid.UUID,
            vacancy_data: VacancyUpdateScheme
    ) -> Vacancy:
        vacancy = await VacancyService.get_vacancy_by_id(session, vacancy_id)

        update_data = vacancy_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(vacancy, field, value)

        await session.commit()
        stmt = (
            select(Vacancy)
            .where(Vacancy.id == vacancy.id)
            .options(selectinload(Vacancy.resumes_replied))
        )
        result = await session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def delete_vacancy(
            session: AsyncSession,
            vacancy_id: uuid.UUID
    ) -> VacancyResponseScheme:
        vacancy = await VacancyService.get_vacancy_by_id(session, vacancy_id)
        await session.delete(vacancy)
        await session.commit()
        return VacancyResponseScheme.model_validate(vacancy)