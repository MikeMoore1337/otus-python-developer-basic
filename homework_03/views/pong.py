from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("/ping/")
def get_answer():
    return {"data": "pong"}
