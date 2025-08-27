from datetime import datetime
from unittest.mock import MagicMock
import uuid
from pytest import fixture


@fixture
def fake_records():
    record_id = uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")
    return [
        MagicMock(
            id = record_id,
            title = "Новая игра",
            player = "Я",
            start_time = datetime.now(),
            end_time = datetime.now(),
            result = "Я выиграл",
            iscancel = False,
            createdat = datetime.now(),
            updatedat = datetime.now()
        ),
        MagicMock(
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
    ]


@fixture
def mock_db_writer(mocker):
    mock = mocker.MagicMock()
    mock.patch("app.repositories.base.DBWriter", return_value=mock)
    return mock


@fixture
def mock_session(mocker, mock_db_writer):
    mock = mocker.MagicMock()
    mock_db_writer.session.return_value.__enter__.return_value = mock
    return mock