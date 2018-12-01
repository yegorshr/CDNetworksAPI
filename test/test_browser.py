import unittest
from unittest.mock import patch, Mock

from cdnetworks import Base, Browser
from test import encode_response
from test.helper import GET_PAD_RESPONSE, GET_API_KEY_RESPONSE, AUTH_TOKEN, PADS, PAD_NOT_FOUND_RESPONSE, \
    RESPONSE_SAM_OK, RESPONSE_SAM_FAILED, CONTRACT_RESPONSE, CONTRACT_RESPONSE_ERROR


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

    def test_get_pad_list_calls_proper_endpoint(self):
        self.request_mock.get.return_value = Mock(ok=True, content=encode_response({'one': 'two'}))

        self.subject.get_pad_list('testToken', 'testApiKey')

        self.request_mock.get.assert_called_once_with(
            params={'sessionToken': 'testToken', 'apiKey': 'testApiKey', 'output': 'json'},
            url='https://openapi.cdnetworks.com/api/rest/pan/site/list', verify=True)

    def test_get_pad_list_raises_error_on_api_error(self):
        self.request_mock.get.return_value = Mock(ok=False, content=encode_response({'one': 'two'}))
        self.request_mock.get.return_value.raise_for_status.side_effect = RuntimeError('CDNetworks API error')
        try:
            self.subject.get_pad_list('testToken', 'testApiKey')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'CDNetworks API error')
        self.request_mock.get.assert_called_once_with(
            params={'sessionToken': 'testToken', 'apiKey': 'testApiKey', 'output': 'json'},
            url='https://openapi.cdnetworks.com/api/rest/pan/site/list', verify=True)

    def test_select_pad_returns_selected_pad(self):
        result = self.subject.select_pad(PADS, 'pad1.cdnet.com')
        self.assertEqual(result, 'pad1.cdnet.com')

    def test_select_pad_returns_exception_on_nonexistent_pad(self):
        try:
            self.subject.select_pad(PADS, 'pad3.cdnet.com')
            self.fail("No exception was thrown")
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), "PAD Name was not found.")

    def test_get_pad_return_pad_if_found(self):
        response = encode_response(GET_PAD_RESPONSE)
        self.request_mock.get.return_value = Mock(ok=True, content=response)
        actual = self.subject.get_pad('testSessionToken', 'test_key', 'testpad')
        self.request_mock.get.assert_called_once_with(params={'sessionToken': 'testSessionToken',
                                                              'apiKey': 'test_key', 'pad': 'testpad',
                                                              'prod': True, 'output': 'json'},
                                                      url='https://openapi.cdnetworks.com/api/rest/pan/site/view',
                                                      verify=True)
        self.assertEqual(actual, GET_PAD_RESPONSE)

    def test_get_pad_raises_exception_if_not_found(self):
        response = encode_response(PAD_NOT_FOUND_RESPONSE)
        self.request_mock.get.return_value = Mock(ok=True, content=response)
        try:
            self.subject.get_pad('testSessionToken', 'test_key', 'testpad')
            self.fail("No exception was thrown")
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), "Invalid PAD supplied.")
        self.request_mock.get.assert_called_once_with(params={'sessionToken': 'testSessionToken',
                                                              'apiKey': 'test_key', 'pad': 'testpad',
                                                              'prod': True, 'output': 'json'},
                                                      url='https://openapi.cdnetworks.com/api/rest/pan/site/view',
                                                      verify=True)

    def test_get_pad_raises_exception_on_api_error(self):
        self.request_mock.get.return_value = Mock(ok=False)
        self.request_mock.get.return_value.raise_for_status.side_effect = RuntimeError('CDNetworks API error')
        try:
            self.subject.get_pad('testSessionToken', 'test_key', 'testpad')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'CDNetworks API error')
        self.request_mock.get.assert_called_once_with(params={'sessionToken': 'testSessionToken',
                                                              'apiKey': 'test_key', 'pad': 'testpad',
                                                              'prod': True, 'output': 'json'},
                                                      url='https://openapi.cdnetworks.com/api/rest/pan/site/view',
                                                      verify=True)

    def test_get_sam_returns_existing_sam(self):
        self.request_mock.get.return_value = Mock(ok=True, content=encode_response(RESPONSE_SAM_OK))

        result = self.subject.get_sam('session_token', 'test_key', 'pad_name')

        self.request_mock.get.assert_called_once_with(
            params={'output': 'json', 'apiKey': 'test_key', 'sessionToken': 'session_token'},
            url='https://openapi.cdnetworks.com/api/rest/pan/sam/pad_name/view', verify=True)
        self.assertEqual(result, RESPONSE_SAM_OK)

    def test_get_sam_raises_error_for_nonexistent_pad(self):
        self.request_mock.get.return_value = Mock(ok=True, content=encode_response(RESPONSE_SAM_FAILED))

        try:
            self.subject.get_sam('session_token', 'test_key', 'non_existent_pad')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), 'You can`t view sam rule on this pad(non_existent_pad).')

    def test_get_sam_raises_error_on_api_error(self):
        self.request_mock.get.return_value = Mock(ok=False, content=encode_response(RESPONSE_SAM_FAILED))
        self.request_mock.get.return_value.raise_for_status.side_effect = RuntimeError('testError')

        try:
            self.subject.get_sam('session_token', 'test_key', 'non_existent_pad')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'testError')

    def test_get_contract_number_returns_contract_number(self):
        self.request_mock.get.return_value = Mock(ok=True, content=encode_response(CONTRACT_RESPONSE))

        result = self.subject.get_contract_number('session_token', 'test_key', 'CA')

        self.request_mock.get.assert_called_once_with(
            params={'sessionToken': 'session_token', 'apiKey': 'test_key', 'output': 'json'},
            url='https://openapi.cdnetworks.com/api/rest/pan/contract/list', verify=True)
        self.assertEqual(result, "123123")

    def test_get_contract_number_raises_error_for_nonexistent_contract(self):
        self.request_mock.get.return_value = Mock(ok=True, content=encode_response(CONTRACT_RESPONSE_ERROR))

        try:
            self.subject.get_contract_number('session_token', 'test_key', 'bad_contract')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), 'error')

    def test_get_sam_raises_error_on_api_error(self):
        self.request_mock.get.return_value = Mock(ok=False, content=encode_response(CONTRACT_RESPONSE_ERROR))

        self.request_mock.get.return_value.raise_for_status.side_effect = RuntimeError('testError')
        try:
            self.subject.get_contract_number('session_token', 'test_key', 'bad_contract')
            self.fail('no exception was thrown')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'testError')
