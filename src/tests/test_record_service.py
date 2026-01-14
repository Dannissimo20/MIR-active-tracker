import copy
import uuid

from pytest import mark, raises
from app.schemas.record_schema import RecordFinish, RecordUpdate
from app.services.record_service import RecordService
from app.utils.errors import RecordUpdateError


@mark.parametrize(
    ("record_id"),
    [uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")],
    ids=["Изменение заголовка у незавершенной записи"]
)
def test_update_unfinished_record(mock_record_repo, fake_records, record_id):
    fake_result = fake_records
    fake_result[0].title = 'New Game'

    mock_record_repo.get_by_id.return_value = fake_result[0]
    mock_record_repo.update.return_value = fake_result

    service = RecordService(mock_record_repo)
    update_request = RecordUpdate(title='New Game')
    
    result = service.update_record(record_id, update_request)

    assert result[0].title == 'New Game'


@mark.parametrize(
    ("record_id"),
    [uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")],
    ids=["Изменение заголовка у завершенной записи"]
)
def test_update_finished_record(mock_record_repo, fake_records, record_id):
    fake_records[0].result = "Win"
    mock_record_repo.get_by_id.return_value = fake_records[0]

    service = RecordService(mock_record_repo)
    update_request = RecordUpdate(title="New Game")

    with raises(RecordUpdateError) as exc_info:
        service.update_record(record_id, update_request)
    
    error = exc_info.value

    assert error.status_code == 409
    mock_record_repo.update.assert_not_called()


@mark.parametrize(
    ("record_id"),
    [uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da")],
    ids=["Завершение незавершенной записи"]
)
def test_finish_correct_record(mock_record_repo, fake_records, record_id):
    mock_record_repo.get_by_id.return_value = fake_records[0]

    res = copy.deepcopy(fake_records)
    res[0].result = "Win"
    mock_record_repo.finish_record.return_value = res

    service = RecordService(mock_record_repo)
    result = service.finish_record(record_id, RecordFinish(result="Win"))

    assert result[0].result == "Win"


@mark.parametrize(
    ("record_id, field_name, field_value"),
    [
        (uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da"), "result", "Win"),
        (uuid.UUID("16fd2706-8baf-433b-82eb-8c7fada847da"), "iscancel", True)
    ],
    ids=[
        'Завершение завершенной записи',
        'Завершение отмененной записи'
    ]
)
def test_finish_incorrect_record(mock_record_repo, fake_records, record_id, field_name, field_value):
    setattr(fake_records[0], field_name, field_value)
    mock_record_repo.get_by_id.return_value = fake_records[0]

    service = RecordService(mock_record_repo)
    with raises(RecordUpdateError) as exc_info:
        service.finish_record(record_id, RecordFinish(result="Win2"))
    error = exc_info.value

    assert error.status_code == 409
    mock_record_repo.finish_record.assert_not_called()
