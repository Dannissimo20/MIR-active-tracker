from datetime import datetime
import uuid
from pydantic import UUID4, ValidationError
from pytest import mark, param, raises
from src.app.schemas.record_schema import BaseSchema, RecordIn, RecordOut, RecordUpdate


@mark.parametrize(
    ('dummy_param'),
    [param(None, id="Проверка параметров базовой схемы")]
)
def test_base_schema_config(dummy_param):
    result = BaseSchema()

    assert result.model_config['from_attributes'] is True
    assert result.model_config['extra'] == 'ignore'


@mark.parametrize(
    ("title, player, start_time, end_time"),
    [
        ("Game", "Player", datetime.now(), datetime.now()),
        ("Game", "Player", "2025-08-04T14:00:00", "2025-08-04T16:00:00"),
        ("Game", "Player", datetime.now(), None),
        ("A" * 255, "B" * 255, datetime.now(), None)
    ],
    ids=[
        "Полностью верный запрос",
        "Запрос с строковым значеним start_time и end_time",
        "Запрос без end_time",
        "Запрос с макисмальным значением длины title и player"
    ]
)
def test_record_in_correct(title: str, player: str, start_time: datetime, end_time: datetime):
    result = RecordIn(title=title, player=player, start_time=start_time, end_time=end_time)

    assert result.title == title
    assert result.player == player
    if not isinstance(start_time, datetime):
        date = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S")
        assert result.start_time == date
    else:
        assert result.start_time == start_time
    if not isinstance(end_time, datetime):
        if result.end_time is None:
            assert True
        else:
            date = datetime.strptime(end_time, "%Y-%m-%dT%H:%M:%S")
            assert result.end_time == date
    else:
        assert result.end_time == end_time


@mark.parametrize(
    ("title, player, start_time, end_time, expected_errors"),
    [
        (123, "Player", datetime.now(), None,
         [{"loc":("title",), "type":"string_type"}]),

        ("A"*256, "Player", datetime.now(), None,
         [{"loc":("title",), "type":"string_too_long"}]),

        ("Game", 123, datetime.now(), None,
         [{"loc":("player",), "type":"string_type"}]),

        ("Game", "B"*256, datetime.now(), None,
         [{"loc":("player",), "type":"string_too_long"}]),
        
        ("Game", "Player", None, None,
         [{"loc":("start_time",), "type":"datetime_type"}]),
        
        ("Game", "Player", datetime.now(), "not_datetime",
         [{"loc":("end_time",), "type":"datetime_from_date_parsing"}]),
    ],
    ids = [
        "Неверный тип title",
        "Длина title первышает 255",
        "Неверный тип player",
        "Длина player превышает 255",
        "Неверный тип start_time",
        "Неверный парсинг end_time"
    ]
)
def test_record_in_incorrect(title: str, player: str, start_time: datetime, end_time: datetime, expected_errors):
    with raises(ValidationError) as exc_info:
        RecordIn(title=title, player=player, start_time=start_time, end_time=end_time)

    errors = exc_info.value.errors()

    expect_error = expected_errors[0]
    actual_error = errors[0]

    assert len(errors) == len(expected_errors)

    assert expect_error['loc'] == actual_error['loc']
    assert expect_error['type'] == actual_error['type']


@mark.parametrize(
    ("title, player, start_time, end_time, result, id, iscancel, createdat, updatedat"),
    [
        ("Game", "Player", datetime.now(), datetime.now(), "Win", uuid.uuid4(), False, datetime.now(), datetime.now()),
        ("Game", "Player", datetime.now(), datetime.now(), None, uuid.uuid4(), False, datetime.now(), datetime.now())
    ],
    ids=[
        "Полностью верный запрос",
        "Запрос с пустым полем result"
    ]
)
def test_record_out_correct(
    title: str,
    player: str,
    start_time: datetime,
    end_time: datetime,
    result: str,
    id: UUID4,
    iscancel: bool,
    createdat: datetime,
    updatedat: datetime
):
    record = RecordOut(
        title=title,
        player=player,
        start_time=start_time,
        end_time=end_time,
        result=result,
        id=id,
        iscancel=iscancel,
        createdat=createdat,
        updatedat=updatedat
    )

    assert record.title == title
    assert record.player == player
    assert record.start_time == start_time
    assert record.end_time == end_time

    if record.result is None:
        assert True
    else:
        assert record.result == result

    assert record.id == id
    assert record.iscancel == iscancel
    assert record.createdat == createdat
    assert record.updatedat == updatedat


@mark.parametrize(
    ("title, player, start_time, end_time, result, id, iscancel, createdat, updatedat, expected_errors"),
    [
        ("Game", "Player", datetime.now(), None, 123, uuid.uuid4(), False, datetime.now(), datetime.now(),
         [{"loc":("result",), "type":"string_type"}]),

        ("Game", "Player", datetime.now(), None, "Win", uuid.uuid1(), False, datetime.now(), datetime.now(),
         [{"loc":("id",), "type":"uuid_version"}]),

        ("Game", "Player", datetime.now(), None, "Win", 123, False, datetime.now(), datetime.now(),
         [{"loc":("id",), "type":"uuid_type"}]),

        ("Game", "Player", datetime.now(), None, "Win", uuid.uuid4(), 123, datetime.now(), datetime.now(),
         [{"loc":("iscancel",), "type":"bool_parsing"}]),
         
        ("Game", "Player", datetime.now(), None, "Win", uuid.uuid4(), None, datetime.now(), datetime.now(),
         [{"loc":("iscancel",), "type":"bool_type"}]),

        ("Game", "Player", datetime.now(), None, "Win", uuid.uuid4(), False, "not-datetime", datetime.now(),
         [{"loc":("createdat",), "type":"datetime_from_date_parsing"}]),
        
        ("Game", "Player", datetime.now(), None, "Win", uuid.uuid4(), False, datetime.now(), "not-datetime",
         [{"loc":("updatedat",), "type":"datetime_from_date_parsing"}])
    ],
    ids=[
        "Неверный тип result",
        "Неверная версия uuid для id",
        "Неверный тип id",
        "Неверный парсинг iscancel",
        "Неверный тип iscancel",
        "Неверный парсинг createdat",
        "Неверный парсинг updatedat",
    ]
)
def test_record_out_incorrect(
    title: str,
    player: str,
    start_time: datetime,
    end_time: datetime,
    result: str,
    id: UUID4,
    iscancel: bool,
    createdat: datetime,
    updatedat: datetime,
    expected_errors
):
    try:
        record = RecordOut(
            title=title,
            player=player,
            start_time=start_time,
            end_time=end_time,
            result=result,
            id=id,
            iscancel=iscancel,
            createdat=createdat,
            updatedat=updatedat
        )
        print(record)
    except Exception as e:
        print(e)
    with raises((ValidationError, )) as exc_info:
        RecordOut(
            title=title,
            player=player,
            start_time=start_time,
            end_time=end_time,
            result=result,
            id=id,
            iscancel=iscancel,
            createdat=createdat,
            updatedat=updatedat
        )
    
    errors = exc_info.value.errors()

    expect_error = expected_errors[0]
    actual_error = errors[0]

    assert len(expected_errors) == len(errors)

    assert expect_error['loc'] == actual_error['loc']
    assert expect_error['type'] == actual_error['type']


@mark.parametrize(
    ("fields_values"),
    [
        {"title": "New title"},
        {"player": "New player"},
        {"start_time": datetime.now()},
        {"title": "A"*255, "player": "B"*255}
    ],
    ids=[
        "Обновление title",
        "Обновление player",
        "Обновление start_time",
        "Обновление title и player значениями с максимальной длинной"
    ]
)
def test_record_update(fields_values: dict):
    result = RecordUpdate.model_validate(fields_values)

    for field, value in fields_values.items():
        assert getattr(result, field) == value
