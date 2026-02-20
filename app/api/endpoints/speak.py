from fastapi import APIRouter

router = APIRouter()

@router.post("/")
async def speak_text():
    return {"message": "Text-to-Speech endpoint"}