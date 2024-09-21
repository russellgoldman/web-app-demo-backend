from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
def hello_world():
    success = True

    if success:
        return {"message": "Hello, World!"}
    else:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": "Something went wrong"}
        )
