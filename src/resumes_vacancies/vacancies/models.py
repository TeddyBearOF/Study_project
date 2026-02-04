import uuid
from typing import Optional

from sqlalchemy import String, Integer
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
        nullable=False
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