from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)

from .base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    hash_password = Column(String(70))

    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    __mapper_args__ = {"eager_defaults": True}
