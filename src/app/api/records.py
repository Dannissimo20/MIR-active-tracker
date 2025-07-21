from fastapi import APIRouter, Depends
from pydantic import UUID4
from src.app.services.record_service import RecordService
from src.app.database.database import DBWriter
from src.app.repositories.record_repo import RecordRepo
from src.app.schemas.record_schema import RecordIn, RecordOut, RecordUpdate

db_writer: DBWriter = DBWriter()


def get_record_repo() -> RecordRepo:
    return RecordRepo(db_writer)

def get_record_service() -> RecordService:
    record_repo: RecordRepo = get_record_repo()
    return RecordService(record_repo)


record_router = APIRouter(
    prefix="/record",
    tags=['Record']
)


@record_router.get("/all-records", response_model=list[RecordOut])
def get_all(record_repo: RecordRepo = Depends(get_record_repo)):
    return record_repo.get_all()


@record_router.get("/all-active-records", response_model=list[RecordOut])
def get_all_active(record_service: RecordService = Depends(get_record_service)):
    return record_service.get_active_records()


@record_router.get("", response_model=RecordOut)
def get_record_by_id(id: UUID4, record_repo: RecordRepo = Depends(get_record_repo)):
    return record_repo.get_by_id(id)


@record_router.post("", response_model=list[RecordOut])
def create_record(request: RecordIn, record_repo: RecordRepo = Depends(get_record_repo)):
    result = record_repo.create(request)
    return result


@record_router.patch(
        "", 
        response_model=list[RecordOut],
        responses={
            200: {"description": "Record updated successfully"},
            409: {"description": "Complete game update error"}
        })
def update_record(id: UUID4, request: RecordUpdate, record_service: RecordService = Depends(get_record_service)):
    result = record_service.update_record(id, request)
    return result


@record_router.delete("", response_model=list[RecordOut])
def cancel_record(id: UUID4, record_repo: RecordRepo = Depends(get_record_repo)):
    result = record_repo.cancel_record(id)
    return result
