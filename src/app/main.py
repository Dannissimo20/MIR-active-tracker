from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def healthcheck():
    return 205