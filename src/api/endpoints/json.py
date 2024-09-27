from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from enum import Enum
from typing import Optional
import json
import os
from src.utils.voice_record_filter import VoiceRecordFilter

router = APIRouter()

@router.get("/records/{start_epoch}/{end_epoch}", status_code=status.HTTP_200_OK)
@router.get(
    "/records/{start_epoch}/{end_epoch}/{record_search_param}/{record_search_value}",
    status_code=status.HTTP_200_OK
)
def get_records(
    start_epoch: int,
    end_epoch: int,
    record_search_param: Optional[str] = None,
    record_search_value: Optional[str] = None
):
    try:
        file_name = "sample_records.json"
        file_path = os.path.join(os.path.dirname(__file__), "../../", file_name)
        voice_record_filter = VoiceRecordFilter(file_path)

        return JSONResponse(content=voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        ))
    except FileNotFoundError as err:
        raise HTTPException(status_code=404, detail=str(err))
    except json.JSONDecodeError as err:
        raise HTTPException(status_code=500, detail=str(err))
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))