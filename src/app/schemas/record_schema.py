from datetime import datetime
from typing import Optional
from pydantic import BaseModel, UUID4


class RecordOut(BaseModel):
    id: UUID4
    title: str
    player: str
    start_time: datetime
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    createdat: datetime
    updatedat: datetime

    class Config:
        from_attributes = True