from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Files(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    path = Column(String(500))
    size = Column(Integer())
    is_downloadable = Column(Boolean())

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("Users")

    __mapper_args__ = {"eager_defaults": True}
