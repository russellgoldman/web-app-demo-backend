import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
import json
from src.main import app
from src.utils.voice_record_filter import VoiceRecordFilter
from src.constants import RecordSearchParam

class TestJSONUnit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = TestClient(app)
    
    @patch('src.api.endpoints.json.VoiceRecordFilter.__init__', return_value=None)
    @patch.object(VoiceRecordFilter, 'filter_records')
    def test_get_records(self, mock_filter_records: MagicMock, mock_init: MagicMock):
        mocked_return_value = [
            {
                "_id": 12345,
                "originationTime": 1656788800,
                "clusterId": "domainserver1",
                "userId": "555666777",
                "devices": {
                    "phone": "SEP123123234234",
                    "voicemail": "555666777VM"
                }
            },
            {
                "_id": 12346,
                "originationTime": 1622548800,
                "clusterId": "domainserver1",
                "userId": "472917482",
                "devices": {
                    "phone": "SEP123123234234",
                    "voicemail": "111222333VM"
                }
            }
        ]
        mock_filter_records.return_value = mocked_return_value
        start_epoch = 1622548800
        end_epoch = 1727044203
        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}')

        self.assertIsInstance(mock_init.call_args[0][0], str)
        mock_filter_records.assert_called_once_with(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=None,
            record_search_value=None
        )
        self.assertEqual(res.json(), mocked_return_value)
        self.assertEqual(res.status_code, 200)
    
    @patch('src.api.endpoints.json.VoiceRecordFilter.__init__', return_value=None)
    @patch.object(VoiceRecordFilter, 'filter_records')
    def test_get_records_with_param(self, mock_filter_records: MagicMock, mock_init: MagicMock):
        mocked_return_value = [
            {
                "_id": 12345,
                "originationTime": 1656788800,
                "clusterId": "domainserver1",
                "userId": "555666777",
                "devices": {
                    "phone": "SEP123123234234",
                    "voicemail": "555666777VM"
                }
            }
        ]
        mock_filter_records.return_value = mocked_return_value
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP123123234234"

        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}/{record_search_param}/{record_search_value}')

        self.assertIsInstance(mock_init.call_args[0][0], str)
        mock_filter_records.assert_called_once_with(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        self.assertEqual(res.json(), mocked_return_value)
        self.assertEqual(res.status_code, 200)

    @patch.object(VoiceRecordFilter, 'filter_records')
    def test_get_records_empty_result(self, mock_filter_records: MagicMock):
        mock_filter_records.return_value = []
        start_epoch = 1622548800
        end_epoch = 1727044203
        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}')

        self.assertEqual(res.json(), [])
        self.assertEqual(res.status_code, 200)
    
    @patch.object(VoiceRecordFilter, 'filter_records')
    def test_get_records_file_not_found(self, mock_filter_records: MagicMock):
        mock_filter_records.side_effect = FileNotFoundError("File not found")
        start_epoch = 1622548800
        end_epoch = 1727044203
        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json(), {"detail": "File not found"})
    
    @patch.object(VoiceRecordFilter, 'filter_records')
    def test_get_records_json_decode_error(self, mock_filter_records: MagicMock):
        mock_filter_records.side_effect = json.JSONDecodeError("Expecting value", "", 0)
        start_epoch = 1622548800
        end_epoch = 1727044203
        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}')

        self.assertEqual(res.status_code, 500)
        self.assertEqual(res.json(), {"detail": "Expecting value: line 1 column 1 (char 0)"})
    
    def test_get_records_invalid_search_param(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = "foo"
        record_search_value = "bar"

        res = self.test_client.get(f'/json/records/{start_epoch}/{end_epoch}/{record_search_param}/{record_search_value}')

        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
