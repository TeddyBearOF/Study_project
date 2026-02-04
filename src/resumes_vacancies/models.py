import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base


class VacancyResume(Base):
    __tablename__ = "vacancies_resumes"

    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('resumes.id', ondelete='CASCADE'),
        primary_key=True
    )

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('vacancies.id', ondelete='CASCADE'),
        primary_key=True
    )

    def __repr__(self) -> str:
        return f"<VacancyResume(resume_id={self.resume_id}, vacancy_id={self.vacancy_id})>"