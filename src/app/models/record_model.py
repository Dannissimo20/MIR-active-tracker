import uuid
from src.app.database.database import Base
from sqlalchemy import UUID, Column, DateTime, String, Boolean,  func


class RecordModel(Base):
    __tablename__ = "record"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    title = Column(String(255), nullable=False)
    player = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    result = Column(String)
    iscancel = Column(Boolean, default=False)
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())
