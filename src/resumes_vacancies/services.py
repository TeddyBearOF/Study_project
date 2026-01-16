import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.resumes_vacancies.models import Resume, Vacancy, VacancyResume
from src.resumes_vacancies.schemas import (
    ResumeCreateScheme, ResumeUpdateScheme,
    VacancyCreateScheme, VacancyUpdateScheme
)


class ResumeService:
    """Сервис для работы с резюме"""

    @staticmethod
    async def create_resume(
            session: AsyncSession,
            resume_data: ResumeCreateScheme
    ) -> Resume:
        """Создание резюме"""
        resume = Resume(
            candidate_name=resume_data.candidate_name,
            main_skill=resume_data.main_skill,
            salary=resume_data.salary
        )
        session.add(resume)
        await session.commit()
        stmt = (
            select(Resume)
            .where(Resume.id == resume.id)
            .options(selectinload(Resume.vacancies_replied))
        )
        result = await session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def get_resume_by_id(
            session: AsyncSession,
            resume_id: uuid.UUID,
            with_vacancies: bool = False
    ) -> Resume:
        """Получение резюме по ID"""
        stmt = select(Resume).where(Resume.id == resume_id)

        stmt = stmt.options(selectinload(Resume.vacancies_replied))

        result = await session.execute(stmt)
        resume = result.scalar_one_or_none()

        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )

        return resume

    @staticmethod
    async def get_resumes(
            session: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            with_vacancies: bool = False
    ) -> List[Resume]:
        """Получение списка резюме"""
        stmt = select(Resume)

        stmt = stmt.options(selectinload(Resume.vacancies_replied))

        stmt = stmt.offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())


    @staticmethod
    async def update_resume(
            session: AsyncSession,
            resume_id: uuid.UUID,
            resume_data: ResumeUpdateScheme
    ) -> Resume:
        """Обновление резюме"""
        resume = await ResumeService.get_resume_by_id(session, resume_id)

        update_data = resume_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(resume, field, value)

        await session.commit()
        stmt = (
            select(Resume)
            .where(Resume.id == resume.id)
            .options(selectinload(Resume.vacancies_replied))
        )
        result = await session.execute(stmt)
        return result.scalar_one()


    @staticmethod
    async def delete_resume(
            session: AsyncSession,
            resume_id: uuid.UUID
    ) -> bool:
        """Удаление резюме (каскадное удаление связей)"""
        resume = await ResumeService.get_resume_by_id(session, resume_id)

        await session.delete(resume)
        await session.commit()
        return True


class VacancyService:
    """Сервис для работы с вакансиями"""

    @staticmethod
    async def create_vacancy(
            session: AsyncSession,
            vacancy_data: VacancyCreateScheme
    ) -> Vacancy:
        """Создание вакансии"""
        vacancy = Vacancy(
            title=vacancy_data.title,
            salary=vacancy_data.salary
        )

        session.add(vacancy)
        await session.commit()

        stmt = (
            select(Vacancy)
            .where(Vacancy.id == vacancy.id)
            .options(selectinload(Vacancy.resumes_replied))
        )
        result = await session.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def get_vacancy_by_id(
            session: AsyncSession,
            vacancy_id: uuid.UUID,
            with_resumes: bool = False
    ) -> Vacancy:
        """Получение вакансии по ID"""
        stmt = (
            select(Vacancy)
            .where(Vacancy.id == vacancy_id)
            .options(selectinload(Vacancy.resumes_replied))
        )

        result = await session.execute(stmt)
        vacancy = result.scalar_one_or_none()

        if not vacancy:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Vacancy not found"
            )

        return vacancy


    @staticmethod
    async def get_vacancies(
            session: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            with_resumes: bool = False
    ) -> List[Vacancy]:
        """Получение списка вакансий"""
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
        """Обновление вакансии"""
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
    ) -> bool:
        """Удаление вакансии (каскадное удаление связей)"""
        vacancy = await VacancyService.get_vacancy_by_id(session, vacancy_id)

        await session.delete(vacancy)
        await session.commit()
        return True


