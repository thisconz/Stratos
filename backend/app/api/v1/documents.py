from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def list_documents():
    return {"message": "List of documents"}
