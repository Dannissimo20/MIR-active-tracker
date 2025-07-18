from fastapi import FastAPI
from src.app.api.records import record_router

app: FastAPI = FastAPI()

app.include_router(record_router)

@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Service is running"}
