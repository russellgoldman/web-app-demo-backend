import unittest
import os
import json
from src.utils.voice_record_filter import VoiceRecordFilter
from src.constants import RecordSearchParam

class TestFilterRecords(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.join(os.path.dirname(__file__), "test_voice_record_filter_integration", "filter_records")

    def test_filter_records_no_search_param_valid_epoch_range(self):
        start_epoch = 1651363200
        end_epoch = 1727044203
        file_path = os.path.join(self.tests_dir, "test_filter_records_no_search_param_valid_epoch_range.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
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
                "_id": 12349,
                "originationTime": 1651363200,
                "clusterId": "domainserver1",
                "userId": "958482928",
                "devices": {
                    "phone": "SEP345678901234",
                    "voicemail": "111222333VM"
                }
            }
        ]

        res = voice_record_filter.filter_records(start_epoch=start_epoch, end_epoch=end_epoch, record_search_param=None, record_search_value=None)
        self.assertEqual(res, expected)

    def test_filter_records_no_search_param_invalid_epoch_range(self):
        start_epoch = 1727044203
        end_epoch = 1622548800
        file_path = os.path.join(self.tests_dir, "test_filter_records_no_search_param_invalid_epoch_range.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        
        with self.assertRaises(ValueError):
            voice_record_filter.filter_records(start_epoch=start_epoch, end_epoch=end_epoch, record_search_param=None, record_search_value=None)

    def test_filter_records_valid_search_param(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.clusterId.value
        record_search_value = "domainserver1"
        file_path = os.path.join(self.tests_dir, "test_filter_records_valid_search_param.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
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
                "_id": 12349,
                "originationTime": 1651363200,
                "clusterId": "domainserver1",
                "userId": "958482928",
                "devices": {
                    "phone": "SEP345678901234",
                    "voicemail": "111222333VM"
                }
            }
        ]

        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        self.assertEqual(res, expected)

    def test_filter_records_invalid_search_param(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = "foo"
        record_search_value = "bar"
        file_path = os.path.join(self.tests_dir, "test_filter_records_invalid_search_param.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
    
        with self.assertRaises(ValueError):
            voice_record_filter.filter_records(
                start_epoch=start_epoch,
                end_epoch=end_epoch,
                record_search_param=record_search_param,
                record_search_value=record_search_value
            )

class TestLoadJson(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.join(os.path.dirname(__file__), "test_voice_record_filter_integration", "_load_json")

    def test_load_json_valid_file(self):
        file_path = os.path.join(self.tests_dir, "test_load_json_valid_file.json")
        VoiceRecordFilter(file_path=file_path)

    def test_load_json_invalid_file_path(self):
        file_path = os.path.join(self.tests_dir, "test_load_json_invalid_file_path.json")
        
        with self.assertRaises(FileNotFoundError):
            VoiceRecordFilter(file_path=file_path)

    def test_load_json_no_search_param_invalid_json_file(self):
        file_path = os.path.join(self.tests_dir, "test_load_json_no_search_param_invalid_json_file.json")
        
        with self.assertRaises(json.JSONDecodeError):
            VoiceRecordFilter(file_path=file_path)

class TestFilterRecord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tests_dir = os.path.join(os.path.dirname(__file__), "test_voice_record_filter_integration", "_filter_record")

    def test_filter_record_origination_time_not_in_record(self):
        start_epoch = 1656788800
        end_epoch = 1727044203
        file_path = os.path.join(self.tests_dir, "test_filter_record_origination_time_not_in_record.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)

        with self.assertRaises(ValueError):
            voice_record_filter.filter_records(
                start_epoch=start_epoch,
                end_epoch=end_epoch,
                record_search_param=None,
                record_search_value=None
            )

    def test_filter_record_origination_time_not_in_epoch_range(self):
        start_epoch = 1700000000
        end_epoch = 1727044203
        file_path = os.path.join(self.tests_dir, "test_filter_record_origination_time_not_in_epoch_range.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch
        )
        expected = []

        self.assertEqual(res, expected)

    def test_filter_devices_not_in_record(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP123123234234"
        file_path = os.path.join(self.tests_dir, "test_filter_devices_not_in_record.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        expected = [
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

        self.assertEqual(res, expected)

    def test_filter_devices_in_record_phone_not_in_devices(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP123123234234"
        file_path = os.path.join(self.tests_dir, "test_filter_devices_in_record_phone_not_in_devices.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        expected = [
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

        self.assertEqual(res, expected)

    def test_filter_phone_and_devices_in_record_phone_not_equal(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP345678901234"
        file_path = os.path.join(self.tests_dir, "test_filter_phone_and_devices_in_record_phone_not_equal.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        expected = []

        self.assertEqual(res, expected)

    def test_filter_phone_and_devices_in_record_phone_equal(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.phone.value
        record_search_value = "SEP345678901234"
        file_path = os.path.join(self.tests_dir, "test_filter_phone_and_devices_in_record_phone_equal.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        expected = [
            {
                "_id": 12349,
                "originationTime": 1651363200,
                "clusterId": "domainserver1",
                "userId": "958482928",
                "devices": {
                    "phone": "SEP345678901234",
                    "voicemail": "111222333VM"
                }
            }
        ]

        self.assertEqual(res, expected)

    def test_filter_devices_in_record_voicemail_not_in_devices(self):
        start_epoch = 1622548800
        end_epoch = 1727044203
        record_search_param = RecordSearchParam.voicemail.value
        record_search_value = "555666777VM"
        file_path = os.path.join(self.tests_dir, "test_filter_devices_in_record_voicemail_not_in_devices.json")
        voice_record_filter = VoiceRecordFilter(file_path=file_path)
        res = voice_record_filter.filter_records(
            start_epoch=start_epoch,
            end_epoch=end_epoch,
            record_search_param=record_search_param,
            record_search_value=record_search_value
        )
        expected = [
            {
                "_id": 12348,
                "originationTime": 1640995200,
                "clusterId": "domainserver2",
                "userId": "555666777",
                "devices": {
                    "phone": "SEP123123234234",
                    "voicemail": "555666777VM"
                }
            }
        ]

        self.assertEqual(res, expected)

    def test_filter_voicemail_and_devices_in_record_voicemail_not_equal(self):
        pass

    def test_filter_voicemail_and_devices_in_record_voicemail_equal(self):
        pass

    def test_filter_userId_not_in_record(self):
        pass

    def test_filter_userId_in_record_userId_not_equal(self):
        pass

    def test_filter_userId_in_record_userId_equal(self):
        pass

    def test_filter_clusterId_not_in_record(self):
        pass

    def test_filter_clusterId_in_record_clusterId_not_equal(self):
        pass

    def test_filter_clusterId_in_record_clusterId_equal(self):
        pass

if __name__ == '__main__':
    unittest.main()
