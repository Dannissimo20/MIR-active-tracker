from typing import Type
import uuid
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
    
        
    def get_active_records(self) -> list[RecordOut]:
        query = select(self._table).where(self._table.iscancel.is_(False))
        with self.db.session() as session:
            res = session.execute(query).scalars().all()
            result = [RecordOut.model_validate(item) for item in res]
            return result


    def cancel_record(self, id: uuid):
        query = update(self._table).where(self._table.id == id).values(iscancel = True)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_all()
