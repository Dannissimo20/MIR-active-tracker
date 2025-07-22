from datetime import datetime
from typing import Type
import uuid
from src.app.utils.errors import RecordUpdateError
from src.app.repositories.base import BaseRepository
from src.app.schemas.record_schema import RecordIn, RecordOut, RecordUpdate
from src.app.models.record_model import RecordModel
from sqlalchemy import func, select, update


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


    def get_active_records(self) -> list[RecordOut]:
        query = select(self._table).where(self._table.iscancel.is_(False)).where(func.date(self._table.start_time) >= datetime.today())
        with self.db.session() as session:
            result = session.execute(query).scalars().all()
            return [self._schema.model_validate(item) for item in result]
