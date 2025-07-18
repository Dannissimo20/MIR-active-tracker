from typing import Type
import uuid
from src.app.schemas.record_schema import RecordIn, RecordOut, RecordUpdate
from src.app.models.record_model import RecordModel
from src.app.database.database import DBWriter
from sqlalchemy import select, insert, update


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
        
    def get_active_records(self) -> list[RecordOut]:
        query = select(self._table).where(self._table.iscancel.is_(False))
        with self.db.session() as session:
            res = session.execute(query).scalars().all()
            result = [RecordOut.model_validate(item) for item in res]
            return result
    
    
    def get_record_by_id(self, id: uuid) -> RecordOut:
        query = select(self._table).where(self._table.id == id)
        with self.db.session() as session:
            res = session.execute(query).scalars().one()
            result = RecordOut.model_validate(res)
            return result


    def add_record(self, request: RecordIn):
        record_data = request.model_dump()
        query = insert(self._table).values(record_data)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_records()
    

    def update_record(self, id: uuid, request: RecordUpdate):
        record_data = request.model_dump(exclude_unset=True)
        query = update(self._table).where(self._table.id == id).values(**record_data)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_records()


    def cancel_record(self, id: uuid):
        query = update(self._table).where(self._table.id == id).values(iscancel = True)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_records()
