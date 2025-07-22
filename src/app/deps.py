from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import Singleton, Factory

from src.app.services.record_service import RecordService
from src.app.database.database import DBWriter
from src.app.repositories.record_repo import RecordRepo


class Container(DeclarativeContainer):
    wiring_config = WiringConfiguration(
        modules=[
            ".api.records"
        ]
    )

    db = Singleton(DBWriter)

    record_repo = Factory(
        RecordRepo, 
        db=db
    )
    
    record_service = Factory(
        RecordService, 
        record_repo=record_repo
    )
