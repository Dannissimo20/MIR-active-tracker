from app.database.database import Base
import binascii
import os
from sqlalchemy import UUID, Boolean, Column, DateTime, String, func


class RecordModel(Base):
    __tablename__ = "record"

    id = Column(
        String(16),
        primary_key=True,
        default=lambda: binascii.hexlify(os.urandom(8)).decode()
    )
    title = Column(String)
    player = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    result = Column(String)
    createdat = Column(DateTime, server_default=func.now())
    updatedat = Column(DateTime, server_default=func.now(), onupdate=func.now())

