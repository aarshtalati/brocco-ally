import unittest
from main import fun_loc, fun_pass, fun_people

class TestIssApiCalls(unittest.TestCase):
    def test_fun_loc_response_length(self):
        _, response = fun_loc(get_http_status_code = True)
        self.assertGreater(len(response), 0, "Function should return message")

    def test_fun_pass_response_length(self):
        _, response  = fun_pass(90.0, -44.0592, get_http_status_code = True)
        self.assertGreater(len(response), 0, "Function should return message")

    def test_fun_people_response_length(self):
        _, response  = fun_people(get_http_status_code = True)
        self.assertGreater(len(response), 0, "Function should return message")

    def test_fun_loc_http_response_status_code(self):
        status, _ = fun_loc(get_http_status_code = True)
        self.assertEqual(status, 200, "Function should return message")

    def test_fun_pass_http_response_status_code(self):
        status, _  = fun_pass(90.0, -44.059, get_http_status_code = True)
        self.assertEqual(status, 200, "Function should return message")

    def test_fun_people_http_response_status_code(self):
        status, _  = fun_people(get_http_status_code = True)
        self.assertEqual(status, 200, "Function should return message")

if __name__ == '__main__':
    unittest.main()
