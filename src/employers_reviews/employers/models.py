import uuid

from sqlalchemy import UUID, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.models import Base


class Employer(Base):
    __tablename__ = 'employers'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )


    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    industry: Mapped[str] = mapped_column(
        String(100)
    )

    location: Mapped[str] = mapped_column(
        String(100)
    )

    reviews: Mapped[list["Review"]] = relationship(
        "Review",
        back_populates="employer",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Employer(id={self.id}, title={self.title})>"