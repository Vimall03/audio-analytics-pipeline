from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def replay_audio():
    return {"message": "Replay endpoint"}