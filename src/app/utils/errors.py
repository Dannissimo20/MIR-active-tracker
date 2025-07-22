from fastapi import HTTPException


class RecordUpdateError(HTTPException):
    """Исключение для ошибок обновления записи"""
    def __init__(
            self,
            status_code = 409,
            detail="CompleteGameUpdateError",
            description: str | None = "Editing a completed game is prohibited"
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.description = description
