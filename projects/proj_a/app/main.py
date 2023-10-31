from fastapi import FastAPI
from hello import hello

app = FastAPI()


@app.get("/")
async def index() -> str:
    return hello("World")
