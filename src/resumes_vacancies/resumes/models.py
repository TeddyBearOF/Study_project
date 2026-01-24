import uuid
from typing import Optional

from sqlalchemy import UUID, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False
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
        return (f"<Resume(id={self.id}, "
                f"candidate_name={self.candidate_name!r}, "
                f"main_skill={self.main_skill!r}, "
                f"salary={self.salary})>")
