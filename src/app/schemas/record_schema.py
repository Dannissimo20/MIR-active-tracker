from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, Field


class RecordIn(BaseModel):
    title: str = Field(max_length=255)
    player: str = Field(max_length=255)
    start_time: datetime = Field(datetime.now())
    end_time: Optional[datetime] = None

    class Config:
        extra = 'ignore'


class RecordOut(RecordIn):
    result: Optional[str] = None
    id: UUID4
    iscancel: bool = False
    createdat: datetime
    updatedat: datetime

    class Config:
        from_attributes = True


class RecordUpdate(BaseModel):
    title: Optional[str] = None
    player: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None

    class Config:
        from_attributes = True
        extra = 'ignore'
