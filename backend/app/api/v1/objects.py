from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_objects():
    return {"message": "List of objects"}