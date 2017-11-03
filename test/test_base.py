import unittest
import json
from cdnetworks.base import Base
from unittest.mock import patch, Mock


class TestBase(unittest.TestCase):
    RESPONSE_LOGIN_SUCCESSFUL = {'loginResponse': {'resultCode': 100}}
    RESPONSE_LOGIN_FAILED = {'loginResponse': {'resultCode': 101}}

    def setUp(self):
        self.args = {
            'username': 'testUsername',
            'password': 'testPassword',
            'verbose': False,
            'svc_group_name': 'testGroupName',
            'svc_name': 'testServiceName'
        }

    @patch('cdnetworks.base.requests')
    def test_login_success_called_with_proper_data(self, request_mock: Mock):
        self.__setup_login(self.RESPONSE_LOGIN_SUCCESSFUL, request_mock)

        request_mock.post.assert_called_once_with(
            data={'output': 'json', 'pass': 'testPassword', 'user': 'testUsername'},
            url='https://openapi.cdnetworks.com/api/rest/login')

    @patch('cdnetworks.base.requests')
    def test_login_success_returns_valid_response(self, request_mock: Mock):
        actual = self.__setup_login(self.RESPONSE_LOGIN_SUCCESSFUL, request_mock)

        self.assertEqual(actual, self.RESPONSE_LOGIN_SUCCESSFUL)

    @patch('cdnetworks.base.requests')
    def test_login_failed_raises_exception(self, request_mock):
        try:
            self.__setup_login(self.RESPONSE_LOGIN_FAILED, request_mock)
            self.fail('should throw')
        except Exception as ve:
            self.assertIsInstance(ve, ValueError)
            self.assertEqual(str(ve), 'User login information is incorrect')

    def __setup_login(self, expected_data, request_mock):
        fake_response = json.dumps(expected_data).encode('utf-8')
        request_mock.post.return_value = Mock(ok=True, content=fake_response)
        args_mock = Mock(**self.args)
        subject = Base(args_mock)
        actual = subject.login()
        return actual


if __name__ == '__main__':
    unittest.main()
