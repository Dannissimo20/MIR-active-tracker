from datetime import datetime
from unittest.mock import MagicMock
import uuid
from pytest import mark, param
from src.app.models.record_model import RecordModel
from src.app.repositories.base import BaseRepository
from src.app.schemas.record_schema import RecordIn, RecordOut, RecordUpdate


class TestRepository(BaseRepository):
    @property
    def _table(self):
        return RecordModel
    
    @property
    def _schema(self):
        return RecordOut


def test_get_all(db_with_data):

    repo = TestRepository(db_with_data)
    records = repo.get_all()

    assert len(records) == 2
    assert records[0].title == "Новая игра"
    assert records[1].title == "НГ+"


def test_get_by_id_with_correct_id(db_with_data):
    record_id = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")

    repo = TestRepository(db_with_data)
    records = repo.get_by_id(record_id) 

    assert records.id == record_id
    assert records.title == "Новая игра"


def test_get_by_id_with_incorrect_id(db_with_data):
    record_id = uuid.UUID("26fd2706-8baf-433b-82eb-8c7fada847da")

    repo = TestRepository(db_with_data)
    records = repo.get_by_id(record_id)

    assert records is None


def test_create(db_with_data):

    fake_add = {
        "title":"Новая игра ++",
        "player":"Я, Он",
        "start_time":datetime.now(),
        "end_time":datetime.now()
    }
    
    record_schema = RecordIn.model_validate(fake_add)
    repo = TestRepository(db_with_data)
    records = repo.create(record_schema)

    assert len(records) == 3
    assert records[0].title == "Новая игра"
    assert records[2].title == "Новая игра ++"


def test_update(db_with_data):
    fake_id = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")

    fake_update = {
        "title": "АБСОЛЮТНО НОВАЯ ИГРА"
    }

    update_schema = RecordUpdate.model_validate(fake_update)

    repo = TestRepository(db_with_data)
    records = repo.update(fake_id, update_schema)

    assert len(records) == 2
    assert records[0].title == "АБСОЛЮТНО НОВАЯ ИГРА"
    assert records[1].title == "НГ+"
