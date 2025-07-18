from fastapi import APIRouter, Depends
from src.app.database.database import DBWriter
from src.app.repositories.record_repo import RecordRepo
from src.app.schemas.record_schema import RecordOut

db_writer: DBWriter = DBWriter()


def get_record_repo() -> RecordRepo:
    return RecordRepo(db_writer)


record_router = APIRouter(
    prefix='/record',
    tags=['Record']
)


@record_router.get("/get_records", response_model=list[RecordOut])
def get_all(record_repo: RecordRepo = Depends(get_record_repo)):
    return record_repo.get_records()
