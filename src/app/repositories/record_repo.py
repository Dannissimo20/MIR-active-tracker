from typing import Type
import uuid
from src.app.utils.errors import RecordUpdateError
from src.app.repositories.base import BaseRepository
from src.app.schemas.record_schema import RecordIn, RecordOut, RecordUpdate
from src.app.models.record_model import RecordModel
from sqlalchemy import select, update


class RecordRepo(BaseRepository[RecordIn, RecordUpdate, RecordOut, RecordModel]):
    @property
    def _table(self) -> Type[RecordModel]:
        return RecordModel
    
    @property
    def _schema(self) -> Type[RecordOut]:
        return RecordOut


    def cancel_record(self, id: uuid):
        query = update(self._table).where(self._table.id == id).values(iscancel = True)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_all()
