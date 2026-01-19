import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status

from src.resumes_vacancies.models import Resume, Vacancy, VacancyResume
from src.resumes_vacancies.schemas import (
    ResumeCreateScheme, ResumeUpdateScheme,
    VacancyCreateScheme, VacancyUpdateScheme
)


class ResumeService:
    @staticmethod
    async def create_resume(
            session: AsyncSession,
            resume_data: ResumeCreateScheme
    ) -> Resume:
        resume = Resume(
            candidate_name=resume_data.candidate_name,
            main_skill=resume_data.main_skill,
            salary=resume_data.salary
        )
        session.add(resume)
        await session.flush()  # чтобы получить resume.id

        # Добавляем связи с вакансиями
        if resume_data.vacancies_replied:
            # Проверим, существуют ли вакансии (опционально)
            select_vacancies_stmt = select(Vacancy.id).where(Vacancy.id.in_(resume_data.vacancies_replied))
            result = await session.execute(select_vacancies_stmt)
            existing_ids = {row[0] for row in result.fetchall()}
            invalid_ids = set(resume_data.vacancies_replied) - existing_ids
            if invalid_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Vacancies not found: {list(invalid_ids)}"
                )

            # Вставляем связи
            insert_stmt = insert(VacancyResume).values([
                {"resume_id": resume.id, "vacancy_id": vid}
                for vid in resume_data.vacancies_replied
            ])
            await session.execute(insert_stmt)

        await session.commit()

        # Возвращаем с загруженными вакансиями
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
            resume_id: uuid.UUID
    ) -> Resume:
        stmt = (
            select(Resume)
            .where(Resume.id == resume_id)
            .options(selectinload(Resume.vacancies_replied))
        )
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
        resume = await ResumeService.get_resume_by_id(session, resume_id)
        await session.delete(resume)
        await session.commit()
        return True


class VacancyService:
    @staticmethod
    async def create_vacancy(
            session: AsyncSession,
            vacancy_data: VacancyCreateScheme
    ) -> Vacancy:
        vacancy = Vacancy(
            title=vacancy_data.title,
            salary=vacancy_data.salary
        )
        session.add(vacancy)
        await session.flush()

        if vacancy_data.resumes_replied:
            select_resumes_stmt = select(Resume.id).where(Resume.id.in_(vacancy_data.resumes_replied))
            result = await session.execute(select_resumes_stmt)
            existing_ids = {row[0] for row in result.fetchall()}
            invalid_ids = set(vacancy_data.resumes_replied) - existing_ids
            if invalid_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Resumes not found: {list(invalid_ids)}"
                )

            insert_stmt = insert(VacancyResume).values([
                {"vacancy_id": vacancy.id, "resume_id": rid}
                for rid in vacancy_data.resumes_replied
            ])
            await session.execute(insert_stmt)

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
            vacancy_id: uuid.UUID
    ) -> Vacancy:
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
    ) -> bool:
        vacancy = await VacancyService.get_vacancy_by_id(session, vacancy_id)
        await session.delete(vacancy)
        await session.commit()
        return True