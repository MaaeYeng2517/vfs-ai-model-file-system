"""Base SQLAlchemy declarative model with common utilities."""
from sqlalchemy.orm import declarative_base, declared_attr
from sqlalchemy import Column, DateTime, func


class TimestampMixin:
    """Mixin adding created_at / updated_at audit columns."""

    @declared_attr
    def created_at(cls):
        return Column(DateTime, server_default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


Base = declarative_base()


def registry():
    return Base.registry