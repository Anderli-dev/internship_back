from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}