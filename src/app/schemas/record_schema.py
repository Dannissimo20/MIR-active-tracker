from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4, Field, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes = True, extra ='ignore')


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
    title: Optional[str] = Field(max_length=255, default=None)
    player: Optional[str] = Field(max_length=255, default=None)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class RecordFinish(BaseSchema):
    result: str
