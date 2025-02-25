from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)