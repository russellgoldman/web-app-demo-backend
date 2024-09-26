from enum import Enum

class RecordSearchParam(str, Enum):
   phone = "phone"
   voicemail = "voicemail"
   userId = "userId"
   clusterId = "clusterId"
