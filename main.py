from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Status": "CI/CD is working!", "Version": 1.0}
