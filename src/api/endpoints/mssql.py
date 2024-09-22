from fastapi import APIRouter, status, Query
from fastapi.responses import JSONResponse
from enum import Enum
from typing import Optional

from src.db.mssql import mssql

router = APIRouter()

class RecordSearchParam(str, Enum):
   phone = "phone"
   voicemail = "voicemail"
   userId = "userId"
   clusterId = "clusterId"

@router.get("/records/{start_epoch}/{end_epoch}", status_code=status.HTTP_200_OK)
def get_records(
   start_epoch: int,
   end_epoch: int,
   record_search_param: Optional[str] = Query(None, alias="record_search_param"),
   record_search_value: Optional[str] = Query(None, alias="record_search_value")
):
   conn = mssql.get_mssql_conn()
   cursor = conn.cursor(as_dict=True)

   query = """
      SELECT
         r.id,
         r.originationTime,
         r.clusterId,
         r.userId,
         utpj.phone,
         utvj.voicemail
      FROM Records AS r
      INNER JOIN UsersToPhonesJunction AS utpj
         ON r.phoneJunctionId = utpj.phoneJunctionId
         AND r.userId = utpj.userId
      INNER JOIN UsersToVoicemailsJunction AS utvj
         ON r.voicemailJunctionId = utvj.voicemailJunctionId
         AND r.userId = utvj.userId
      WHERE originationTime BETWEEN %s AND %s
   """

   if record_search_param is not None:
      if RecordSearchParam.phone == record_search_param:
         query += " AND utpj.phone = %s"
      elif RecordSearchParam.voicemail == record_search_param:
         query += " AND utvj.voicemail = %s"
      elif RecordSearchParam.userId == record_search_param:
         query += " AND r.userId = %s"
      elif RecordSearchParam.clusterId == record_search_param:
         query += " AND r.clusterId = %s"
   
      cursor.execute(
         query,
         (start_epoch, end_epoch, record_search_value)
      )
   else:
      cursor.execute(
         query,
         (start_epoch, end_epoch)
      )

   records = cursor.fetchall()
   conn.close()

   return JSONResponse(content=records)
