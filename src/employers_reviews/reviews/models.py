import uuid

from sqlalchemy import String, Integer, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.models import Base


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    employer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('employers.id', ondelete="CASCADE"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    stars: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    employer: Mapped["Employer"] = relationship(
        "Employer",
        back_populates="reviews"
    )

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, employer_id={self.employer_id}, stars={self.stars})>"