from typing import Annotated

from fastapi import FastAPI, Query
from views import calc_router, items_router, pong_router

app = FastAPI()
app.include_router(items_router)
app.include_router(calc_router)
app.include_router(pong_router)


@app.get("/")
def hello_index():
    return {"message": "Hello World!"}


@app.get("/hello/")
def hello_user(name: Annotated[str, Query(min_length=3)]):
    return {"message": f"Hello {name}!"}


@app.get("/hello/{name}/")
def hello_user_path(name: str):
    return {"message": f"Hello {name}!!!"}
