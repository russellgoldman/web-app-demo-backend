import unittest
from fastapi.testclient import TestClient
from src.main import app
from src.constants import RecordSearchParam

class TestJSONIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_client = TestClient(app)

    def test_get_records(self):
        start_epoch = 1656788800
        end_epoch = 1727044203
        res = self.test_client.get(f"/json/records/{start_epoch}/{end_epoch}")
        expected = [
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
        
        self.assertEqual(res.json(), expected)
        self.assertEqual(res.status_code, 200)

    def test_get_records_with_param(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP123123234234"
        res = self.test_client.get(f"/json/records/{start_epoch}/{end_epoch}/{record_search_param}/{record_search_value}")
        expected = [
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
            },
            {
                "_id": 12348,
                "originationTime": 1640995200,
                "clusterId": "domainserver2",
                "userId": "555666777",
                "devices": {
                    "phone": "SEP123123234234",
                    "voicemail": "555666777VM"
                }
            },
        ]

        self.assertEqual(res.json(), expected)
        self.assertEqual(res.status_code, 200)

    def test_get_records_empty_result(self):
        start_epoch = 1727044202
        end_epoch = 1727044203
        res = self.test_client.get(f"/json/records/{start_epoch}/{end_epoch}")
        expected = []

        self.assertEqual(res.json(), expected)
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()
