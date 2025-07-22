from fastapi import FastAPI
from src.app.deps import Container
from src.app.api.records import record_router

app: FastAPI = FastAPI()
container: Container = Container()
app.container = container

app.include_router(record_router)


@app.get("/")
def healthcheck():
    return {"status": "ok", "message": "Service is running"}
