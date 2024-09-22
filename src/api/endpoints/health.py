from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def health():
    return {"message": "Healthy"}
