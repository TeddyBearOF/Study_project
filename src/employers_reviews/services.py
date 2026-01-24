import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.employers_reviews.employers.models import Employer
from src.employers_reviews.employers.schemas import EmployerCreate, EmployerUpdate
from src.employers_reviews.reviews.models import Review
from src.exceptions import EntityNotFoundException, InvalidInputDataException




class EmployerService:
    @staticmethod
    async def get_employer_by_id(db: AsyncSession, employer_id: UUID) -> Employer:
        stmt = (
            select(Employer)
            .where(Employer.id == employer_id)
            .options(selectinload(Employer.reviews))
        )
        result = await db.execute(stmt)
        employer = result.scalar_one_or_none()

        if not employer:
            raise EntityNotFoundException("Employer", str(employer_id))

        return employer

    @staticmethod
    async def create_employer(db: AsyncSession, employer_data: EmployerCreate) -> Employer:
        employer = Employer(
            id=uuid.uuid4(),
            title=employer_data.title,
            industry=employer_data.industry,
            location=employer_data.location
        )

        if employer_data.reviews:
            for review_data in employer_data.reviews:
                if review_data.stars < 1 or review_data.stars > 5:
                    raise InvalidInputDataException("Stars must be between 1 and 5")
                review = Review(
                    title=review_data.title,
                    stars=review_data.stars
                )
                employer.reviews.append(review)

        db.add(employer)
        await db.commit()
        await db.refresh(employer)

        stmt = (
            select(Employer)
            .where(Employer.id == employer.id)
            .options(selectinload(Employer.reviews))
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def update_employer(
            db: AsyncSession,
            employer: Employer,
            employer_data: EmployerUpdate
    ) -> Employer:
        update_data = employer_data.model_dump(exclude_unset=True, exclude={"reviews"})
        for field, value in update_data.items():
            setattr(employer, field, value)

        if employer_data.reviews is not None:
            employer.reviews.clear()
            for review_data in employer_data.reviews:
                if review_data.stars < 1 or review_data.stars > 5:
                    raise InvalidInputDataException("Stars must be between 1 and 5")
                review = Review(
                    title=review_data.title,
                    stars=review_data.stars
                )
                employer.reviews.append(review)

        await db.commit()
        await db.refresh(employer)

        stmt = (
            select(Employer)
            .where(Employer.id == employer.id)
            .options(selectinload(Employer.reviews))
        )
        result = await db.execute(stmt)
        return result.scalar_one()

    @staticmethod
    async def delete_employer(db: AsyncSession, employer: Employer) -> None:
        await db.delete(employer)
        await db.commit()