from app.database.database import Base
import binascii
import os
from sqlalchemy import UUID, Boolean, Column, DateTime, String, func


class RecordModel(Base):
    __tablename__ = "record"

    id = Column(
        UUID,
        primary_key=True
    )
    title = Column(String(255), nullable=False)
    player = Column(String(255), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    result = Column(String)
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

