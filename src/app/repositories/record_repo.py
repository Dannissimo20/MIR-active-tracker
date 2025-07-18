from typing import Type
from src.app.schemas.record_schema import RecordOut
from src.app.models.record_model import RecordModel
from src.app.database.database import DBWriter
from sqlalchemy import select


class RecordRepo:
    def __init__(self, db: DBWriter):
        self.db: DBWriter = db

    @property
    def _table(self) -> Type[RecordModel]:
        return RecordModel
    
    def get_records(self) -> list[RecordOut]:
        query = select(self._table)
        with self.db.session() as session:
            res = session.execute(query).scalars().all()
            result = [RecordOut.model_validate(item) for item in res]
            return result
