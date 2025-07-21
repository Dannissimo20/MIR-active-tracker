import abc
from typing import Generic, Type, TypeVar
import uuid

from sqlalchemy import insert, select, update

from src.app.database.database import DBWriter

IN_SCHEMA = TypeVar("IN_SCHEMA")
UPDATE_SCHEMA = TypeVar("UPDATE_SCHEMA")
SCHEMA = TypeVar("SCHEMA")
TABLE = TypeVar("TABLE")

class BaseRepository(Generic[IN_SCHEMA, UPDATE_SCHEMA, SCHEMA, TABLE], metaclass=abc.ABCMeta):
    def __init__(self, db: DBWriter):
        self.db: DBWriter = db

    @property
    @abc.abstractmethod
    def _table(self) -> Type[TABLE]:
        pass

    @property
    @abc.abstractmethod
    def _schema(self) -> Type[SCHEMA]:
        pass


    def get_all(self) -> list[SCHEMA]:
        query = select(self._table)
        with self.db.session() as session:
            result = session.execute(query).scalars().all()
            return [self._schema.model_validate(item) for item in result]


    def get_by_id(self, id: uuid) -> SCHEMA:
        query = select(self._table).where(self._table.id == id)
        with self.db.session() as session:
            result = session.execute(query).scalars().first()
            return self._schema.model_validate(result)


    def create(self, request: IN_SCHEMA) -> list[SCHEMA]:
        data = request.model_dump()
        query = insert(self._table).values(data)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_all()


    def update(self, id: uuid, request: UPDATE_SCHEMA) -> list[SCHEMA]:
        data = request.model_dump(exclude_unset=True)
        query = update(self._table).where(self._table.id == id).values(**data)
        with self.db.session() as session:
            session.execute(query)
            session.commit()
            return self.get_all()