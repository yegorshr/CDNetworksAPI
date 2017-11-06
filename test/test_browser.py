import unittest
import json
from cdnetworks import Base, Browser
from unittest.mock import patch, Mock
from test import encode_response

GET_API_KEY_RESPONSE = {
    'apiKeyInfo': {
        'returnCode': 0,
        'apiKeyInfoItem': [{'apiKey': 'SERVICECATEGORY_CA',
                            'serviceName': 'Content Acceleration',
                            'parentApiKey': 'SERVICECATEGORY_CA',
                            'type': 0
                            },
                           {'apiKey': 'TEST_API_KEY',
                            'serviceName': 'service2',
                            'parentApiKey': 'SERVICECATEGORY_CA',
                            'type': 1
                            }]
    }
}

AUTH_TOKEN = {'loginResponse': {
    'session': [
        {
            'sessionToken': 'testSessionToken',
            'svcGroupName': 'existing_service_group',
            'svcGroupIdentifier': 'testSvcGroupIdentifier'
        },
        {
            'sessionToken': 'token2',
            'svcGroupName': 'svc_group_2',
            'svcGroupIdentifier': 'svc_group_id2'
        }],
    'resultCode': 0}}


class TestBrowser(unittest.TestCase):
    def setUp(self):
        self.request_mock = patch('cdnetworks.base.requests').start()
        self.subject = Browser(Base(username='testUsername', password='testPassword', verbose=False))

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_get_api_key_returns_api_key_when_called_with_existing_service_name(self):
        response = encode_response(GET_API_KEY_RESPONSE)
        self.request_mock.get.return_value = Mock(ok=True, content=response)

        actual = self.subject.get_api_key_for_service('testSessionToken', 'SERVICECATEGORY_CA')

        self.request_mock.get.assert_called_once_with(params={'output': 'json', 'sessionToken': 'testSessionToken'},
                                                      url='https://openapi.cdnetworks.com/api/rest/getApiKeyList',
                                                      verify=True)

        self.assertEqual(actual, 'SERVICECATEGORY_CA')

    def test_get_api_key_raises_exception_when_called_with_non_existent_service_name(self):
        response = encode_response(GET_API_KEY_RESPONSE)
        self.request_mock.get.return_value = Mock(ok=True, content=response)
        try:
            self.subject.get_api_key_for_service('testSessionToken', 'maunika')
            self.fail('no value error was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), 'Service Name was not found.')

    def test_get_api_key_raises_error_for_api_error(self):
        response = encode_response(GET_API_KEY_RESPONSE)
        self.request_mock.get.return_value = Mock(ok=False, content=response)
        self.request_mock.get.return_value.raise_for_status.side_effect = RuntimeError('CDNetworks API error')

        try:
            self.subject.get_api_key_for_service('testSessionToken', 'maunika')
            self.fail('no value error was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'CDNetworks API error')

    def test_get_token_for_control_group_returns_session_token_for_existing_control_group(self):
        actual = self.subject.get_token_for_control_group(AUTH_TOKEN, 'existing_service_group')
        self.assertEqual(actual, 'testSessionToken')

    def test_get_token_for_control_group_raises_error_for_non_existent_control_group(self):
        try:
            self.subject.get_token_for_control_group(AUTH_TOKEN, 'non_existing')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), 'Group Name was not found.')


if __name__ == '__main__':
    unittest.main()
