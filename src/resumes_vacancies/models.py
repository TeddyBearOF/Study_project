import uuid
from typing import Optional

from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Vacancy(Base):
    __tablename__ = "vacancies"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    salary: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable = True
    )

    resumes_replied: Mapped[list["Resume"]] = relationship(
        'Resume',
        back_populates="vacancies_replied",
        secondary="vacancies_resumes",
        cascade='all, delete'
    )

    def __repr__(self) -> str:
        return f"<Vacancy(id={self.id}, title={self.title!r}, salary={self.salary})>"


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
        index=True
    )

    candidate_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    main_skill: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    salary: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable = True
    )

    vacancies_replied: Mapped[list["Vacancy"]] = relationship(
        'Vacancy',
        back_populates="resumes_replied",
        secondary="vacancies_resumes",
        cascade="all, delete"
    )

    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, candidate_name={self.candidate_name!r}, main_skill={self.main_skill!r}, salary={self.salary})>"


class VacancyResume(Base):
    __tablename__ = "vacancies_resumes"

    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('resumes.id', ondelete='CASCADE'),
        primary_key=True,
        index=True
    )

    vacancy_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('vacancies.id', ondelete='CASCADE'),
        primary_key=True,
        index=True
    )

    def __repr__(self) -> str:
        return f"<VacancyResume(resume_id={self.resume_id}, vacancy_id={self.vacancy_id})>"