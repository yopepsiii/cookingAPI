import uuid
from datetime import datetime

from sqlalchemy import types, text, func, ForeignKey
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id: Mapped[uuid.UUID] = mapped_column(
        types.Uuid, server_default=text("gen_random_uuid()"), primary_key=True
    )

    username: Mapped[str] = mapped_column()  # не уверен насчет этого
    email: Mapped[str] = mapped_column(unique=True)

    password: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(nullable=True)

    best_score: Mapped['Score'] = relationship(lazy='selectin', cascade='all, delete-orphan')


class Score(Base):
    __tablename__ = "Scores"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, server_default=text("gen_random_uuid()"))

    value: Mapped[float] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(nullable=True)

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('Users.id', ondelete='CASCADE'), unique=True)
    user: Mapped['User'] = relationship(lazy='selectin', back_populates="best_score", single_parent=True, cascade='all, delete-orphan')
