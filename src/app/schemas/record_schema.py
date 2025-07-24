from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, Field


class BaseSchema(BaseModel):
    class Config:
        extra = 'ignore'
        from_attributes = True


class RecordIn(BaseSchema):
    title: str = Field(max_length=255)
    player: str = Field(max_length=255)
    start_time: datetime = Field(datetime.now())
    end_time: Optional[datetime] = None


class RecordOut(RecordIn):
    result: Optional[str] = None
    id: UUID4
    iscancel: bool = False
    createdat: datetime
    updatedat: datetime


class RecordUpdate(BaseSchema):
    title: Optional[str] = None
    player: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class RecordFinish(BaseSchema):
    result: str
