from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home() -> dict:
    return {"status_code": 200, "detail": "ok", "result": "working"}

if __name__ == "__main__":
    # To make the work more comfortable, you can run a script. 
    # It is better to do this in a separate file like run.py.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)