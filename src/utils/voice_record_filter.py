import json
from typing import List, Dict, Optional
from src.constants import RecordSearchParam

class VoiceRecordFilter:
    """
    This class is used to perform filter operations on a JSON file
    containing voice records.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.load_json()
    
    def load_json(self):
        try:
            with open(self.file_path, 'r') as f:
                self.records = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"The JSON file path '{self.file_path}' could not be found")
        except json.JSONDecodeError:
            raise ValueError("An unexpected error occurred while decoding the JSON file")

    def filter_records(
        self,
        start_epoch: int,
        end_epoch: int,
        record_search_param: Optional[str] = None,
        record_search_value: Optional[str] = None
    ) -> List[Dict]:
        # The below condition will only occur if `load_immediate` in the __init__ method is overriden to False
        # and the caller has not yet invoked the `load_json` method.
        if self.records is None:
            raise ValueError("The JSON data has not yet been loaded. Please be sure to invoke the 'load_json' method before invoking this method.")

        def filter_record(record: Dict) -> bool:            
            # Since start_epoch and end_epoch are required parameters, I have deduced that "originationTime" must be present in every valid record
            if "originationTime" not in record:
                raise ValueError("Every record in the JSON file is expected to contain an 'originationTime'. Please verify and try again.")

            if not (start_epoch <= record["originationTime"] <= end_epoch):
                return False

            if record_search_param is not None:
                if record_search_param == RecordSearchParam.phone:
                    if not ("devices" in record and "phone" in record["devices"] and record_search_value == record["devices"]["phone"]):
                        return False
                if record_search_param == RecordSearchParam.voicemail:
                    if not ("devices" in record and "voicemail" in record["devices"] and record_search_value == record["devices"]["voicemail"]):
                        return False
                if record_search_param == RecordSearchParam.userId:
                    if not ("userId" in record and record_search_value == record["userId"]):
                        return False
                if record_search_param == RecordSearchParam.clusterId:
                    if not ("clusterId" in record and record_search_value == record["clusterId"]):
                        return False
            
            return True
                
        return [record for record in self.records if filter_record(record)]
