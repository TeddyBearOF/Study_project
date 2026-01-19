from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.models import Base


class Employer(Base):
    __tablename__ = 'employers'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
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

class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True)

    employer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('employers.id', ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    stars: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )

    employer: Mapped["Employer"] = relationship(
        "Employer",
        back_populates="reviews"
    )

    def __repr__(self) -> str:
        return f"<Review(id={self.id}, employer_id={self.employer_id}, stars={self.stars})>"