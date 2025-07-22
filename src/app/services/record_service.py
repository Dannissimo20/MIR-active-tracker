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
