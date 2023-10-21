from fastapi import APIRouter

router = APIRouter(prefix="/ping", tags=["Ping"])


@router.get("/")
def get_answer():
    return {"data": "pong"}
