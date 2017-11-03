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
        self.request_mock = patch('cdnetworks.base.requests').start()

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_login_success_called_with_proper_data(self):
        self.__setup_login(self.RESPONSE_LOGIN_SUCCESSFUL)

        self.request_mock.post.assert_called_once_with(
            data={'output': 'json', 'pass': 'testPassword', 'user': 'testUsername'},
            url='https://openapi.cdnetworks.com/api/rest/login')

    def test_login_success_returns_valid_response(self):
        actual = self.__setup_login(self.RESPONSE_LOGIN_SUCCESSFUL)

        self.assertEqual(actual, self.RESPONSE_LOGIN_SUCCESSFUL)

    def test_login_failed_raises_exception(self):
        try:
            self.__setup_login(self.RESPONSE_LOGIN_FAILED)
            self.fail('should throw')
        except Exception as ve:
            self.assertIsInstance(ve, ValueError)
            self.assertEqual(str(ve), 'User login information is incorrect')

    def __setup_login(self, expected_data):
        fake_response = json.dumps(expected_data).encode('utf-8')
        self.request_mock.post.return_value = Mock(ok=True, content=fake_response)
        args_mock = Mock(**self.args)
        subject = Base(args_mock)
        actual = subject.login()
        return actual


if __name__ == '__main__':
    unittest.main()
