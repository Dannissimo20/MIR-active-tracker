from datetime import datetime
import uuid
import pytest

from src.app.database.database import Base, DBWriter
from src.app.models.record_model import RecordModel
from src.app.repositories.base import BaseRepository
from src.app.schemas.record_schema import RecordOut
from src.tests.test_base_repo import TestRepository

@pytest.fixture
def db_with_data():
    db: DBWriter = DBWriter('sqlite:///:memory:')
    Base.metadata.create_all(db.engine)

    with db.session() as session:
        record_id = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")
        record = RecordModel(
            id = record_id,
            title = "Новая игра",
            player = "Я",
            start_time = datetime.now(),
            end_time = datetime.now(),
            result = "Я выиграл",
            iscancel = False,
            createdat = datetime.now(),
            updatedat = datetime.now()
        )
        session.add(record)
        record = RecordModel(
            id = uuid.uuid4(),
            title = "НГ+",
            player = "Я, Он",
            start_time = datetime.now(),
            end_time = None,
            result = None,
            iscancel = False,
            createdat = datetime.now(),
            updatedat = datetime.now()
        )
        session.add(record)
        session.flush()
    yield db
