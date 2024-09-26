import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from src.main import app
from src.utils.voice_record_filter import VoiceRecordFilter

class TestJSONUnit(unittest.TestCase):
    def setUp(self):
        self.test_client = TestClient(app)
    
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

if __name__ == '__main__':
    unittest.main()
