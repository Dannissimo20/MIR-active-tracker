from datetime import datetime
import uuid
from app.utils.errors import RecordUpdateError
from src.app.repositories.record_repo import RecordRepo
from src.app.schemas.record_schema import RecordOut, RecordUpdate


class RecordService:
    def __init__(self, record_repo: RecordRepo):
        self.record_repo = record_repo


    def update_record(self, id: uuid, request: RecordUpdate) -> list[RecordOut]:
        record_for_update: RecordOut = self.record_repo.get_by_id(id)
        if record_for_update.result is not None:
            raise RecordUpdateError()
        result: list[RecordOut] = self.record_repo.update(id, request)
        return result
    

    def get_active_records(self) -> list[RecordOut]:
        records: list[RecordOut] = self.record_repo.get_all()
        result: list[RecordOut] = []
        for item in records:
            if item.iscancel is False:
                if item.end_time is not None:
                    if item.end_time >= datetime.now():
                        result.append(item)
                else:
                    if item.start_time.date() >= datetime.now().date():
                        result.append(item)
        return result