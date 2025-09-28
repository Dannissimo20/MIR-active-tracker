from datetime import datetime
from unittest.mock import MagicMock
import uuid
from pytest import mark, param
from src.app.models.record_model import RecordModel
from src.app.repositories.base import BaseRepository
from src.app.schemas.record_schema import RecordOut


class TestRepository(BaseRepository):
    @property
    def _table(self):
        return RecordModel
    
    @property
    def _schema(self):
        return RecordOut

@mark.parametrize(
    ("dummy_param"),
    [param(None, id = "Получение всех записей при пустой бд")],
)
def test_get_all_empty(mock_session, mock_db_writer, dummy_param):
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    repo = TestRepository(mock_db_writer)
    records = repo.get_all()

    assert len(records) == 0


@mark.parametrize(
    ("dummy_param"),
    [param(None, id = "Получение всех записей")],
)
def test_get_all(mock_session, mock_db_writer, fake_records, dummy_param):
    mock_session.execute.return_value.scalars.return_value.all.return_value = fake_records

    repo = TestRepository(mock_db_writer)
    records = repo.get_all()

    assert len(records) == 2
    assert records[0].title == "Новая игра"
    assert records[1].title == "НГ+"


@mark.parametrize(
    ("record_id"),
    [param(uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da"), id = "Получение записи с существующим id")],
)
def test_get_by_id_with_correct_id(mock_db_writer, mock_session, fake_records, record_id):
    mock_session.execute.return_value.scalars.return_value.first.return_value = fake_records[0]

    repo = TestRepository(mock_db_writer)
    records = repo.get_by_id(record_id) 

    assert records.id == record_id
    assert records.title == "Новая игра"


@mark.parametrize(
    ("record_id"),
    [param(uuid.UUID("26fd2706-8baf-433b-82eb-8c7fada847da"), id = "Получение записи с существующим id")],
)
def test_get_by_id_with_incorrect_id(mock_db_writer, mock_session, record_id):
    mock_session.execute.return_value.scalars.return_value.first.return_value = None

    repo = TestRepository(mock_db_writer)
    records = repo.get_by_id(record_id)

    assert records is None

@mark.parametrize(
    ("record_id"),
    [param(uuid.uuid4(), id = "Создание записи")],
)
def test_create(mock_session, mock_db_writer, fake_records, record_id):
    record_id = uuid.uuid4()
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        *fake_records,
        MagicMock(
            id = record_id,
            title = "Новая игра ++",
            player = "Я, Он",
            start_time = datetime.now(),
            end_time = datetime.now(),
            result = None, 
            iscancel = False, 
            createdat = datetime.now(), 
            updatedat = datetime.now()
        )
    ]

    fake_add = {
        "title":"Новая игра ++",
        "player":"Я, Он",
        "start_time":datetime.now(),
        "end_time":datetime.now()
    }
    request_mock = MagicMock()
    request_mock.model_dump.return_value = fake_add

    repo = TestRepository(mock_db_writer)
    records = repo.create(request_mock)

    assert mock_session.execute.call_count == 2
    mock_session.commit.assert_called_once()
    assert len(records) == 3
    assert records[0].title == "Новая игра"
    assert records[2].title == "Новая игра ++"


@mark.parametrize(
    ("record_id"),
    [param(uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da"), id = "Обновление записи")],
)
def test_update(mock_db_writer, mock_session, fake_records, record_id):
    fake_records[0].title = "АБСОЛЮТНО НОВАЯ ИГРА"
    mock_session.execute.return_value.scalars.return_value.all.return_value = fake_records

    fake_update = {
        "title": "АБСОЛЮТНО НОВАЯ ИГРА"
    }

    mock_request = MagicMock()
    mock_request.model_dump.return_value = fake_update

    repo = TestRepository(mock_db_writer)
    records = repo.update(record_id, mock_request)

    assert mock_session.execute.call_count == 2
    assert len(records) == 2
    assert records[0].title == "АБСОЛЮТНО НОВАЯ ИГРА"
    assert records[1].title == "НГ+"
