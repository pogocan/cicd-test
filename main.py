from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "Look Ma, no hands!", "Version": "2.0-Automatic"}
