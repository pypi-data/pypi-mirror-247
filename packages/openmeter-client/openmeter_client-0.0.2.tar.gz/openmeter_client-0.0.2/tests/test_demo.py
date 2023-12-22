import unittest
from openmeter import OpenMeterClient


class TestOpenMeterClient(unittest.TestCase):

    def setUp(self):
        self.demo_api_key = '969AC556-9185-48B2-97D2-D72341911067'
        self.demo_sensor_id = '78347197-77dc-4861-ae1f-19f21a6ff510'
        self.client = OpenMeterClient(personal_access_token=self.demo_api_key)

    def test_api_key_is_set(self):
        self.assertEqual(self.client.api_key, self.demo_api_key)

    def test_api_status(self):
        self.assertEqual(self.client.api_status(), "OK")

    def test_get_meta_data_without_page(self):
        results_list = self.client.get_meta_data(page=0)
        result = len(results_list)
        expected_result =  10
        self.assertEqual(result, expected_result)

    def test_get_meta_data_with_page(self):
        results_list = self.client.get_meta_data(page=1)
        result = len(results_list)
        expected_result = 10
        self.assertEqual(result, expected_result)

    def test_get_meta_data_with_filters(self):
        results_list = self.client.get_meta_data(sensor_id=self.demo_sensor_id)
        result = len(results_list)
        expected_result = 1
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()