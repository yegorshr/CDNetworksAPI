import unittest
import cdnetworks
from unittest.mock import patch, Mock
from test.helper import encode_response, GET_PAD_RESPONSE, ADD_PAD_ALIAS_FAILED_RESPONSE


class TestActions(unittest.TestCase):
    def setUp(self):
        self.args = {
            'username': 'testUsername',
            'password': 'testPassword',
            'verbose': False,
            'svc_group_name': 'testGroupName',
            'svc_name': 'testServiceName'
        }
        self.request_mock = patch('cdnetworks.base.requests').start()
        self.api_base = cdnetworks.Base(self.args['username'], self.args['password'])

        self.subject = cdnetworks.Actions(self.api_base, 'testSessionToken', 'testApiKey')

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_clone_pad_calls_proper_endpoint(self):
        expected_response = {}
        self.request_mock.post.return_value = Mock(ok=True, content=encode_response(expected_response))
        result = self.subject.clone_pad('testContractNo', 'testSrcPad', 'testNewPad', 'testOrigin', 'testDescription')

        assert isinstance(self.request_mock.post, Mock)
        self.request_mock.post.assert_called_once_with(data={
            'output': 'json',
            'sessionToken': 'testSessionToken',
            'copy_settings_from': 'testSrcPad',
            'apiKey': 'testApiKey',
            'pad': 'testNewPad',
            'origin': 'testOrigin',
            'product': 'testContractNo',
            'description': 'testDescription'}, url='https://openapi.cdnetworks.com/api/rest/pan/site/v2/add')
        self.assertEqual(result, expected_response)

    def test_clone_pad_raises_error_on_api_error(self):
        post_mock = self.request_mock.post
        post_mock.return_value = Mock(ok=False, content=encode_response({}))
        post_mock.return_value.raise_for_status.side_effect = RuntimeError('error')

        try:
            self.subject.clone_pad('testContract', 'testSrcPad', 'testNewPad', 'testOrigin', 'testDescription')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'error')

    def test_add_alias_to_pad_returns_modified_pad(self):
        self.request_mock.post.return_value = Mock(ok=True, content=encode_response(GET_PAD_RESPONSE))

        result = self.subject.add_alias_to_pad(GET_PAD_RESPONSE, 'testPadName', 'testDomain')

        aliases = result['PadConfigResponse']['data']['data']['pad_aliases'].split('\n')
        self.assertIn('testDomain', aliases)
        self.assertIn('alias1.url.com', aliases)

    def test_add_alias_to_pad_calls_proper_endpoint(self):
        self.request_mock.post.return_value = Mock(ok=True, content=encode_response(GET_PAD_RESPONSE))
        self.subject.add_alias_to_pad(GET_PAD_RESPONSE, 'testPadName', 'testDomain')

        self.request_mock.post.assert_called_once_with(data={
            'output': 'json',
            'sessionToken': 'testSessionToken',
            'apiKey': 'testApiKey',
            'pad_aliases': 'alias1.url.com\ntestDomain',
            'pad': 'testPadName'}, url='https://openapi.cdnetworks.com/api/rest/pan/site/v2/edit')

    def test_add_alias_to_pad_raises_error_on_api_error(self):
        post_mock = self.request_mock.post
        post_mock.return_value = Mock(ok=False, content=encode_response(GET_PAD_RESPONSE))
        post_mock.return_value.raise_for_status.side_effect = RuntimeError('error')

        try:
            self.subject.add_alias_to_pad(GET_PAD_RESPONSE, 'testPadName', 'testDomain')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'error')

    def test_add_alias_to_pad_raises_error_on_bad_request(self):
        post_mock = self.request_mock.post
        post_mock.return_value = Mock(ok=True, content=encode_response(ADD_PAD_ALIAS_FAILED_RESPONSE))
        post_mock.return_value.raise_for_status.side_effect = RuntimeError('error')

        try:
            self.subject.add_alias_to_pad(GET_PAD_RESPONSE, 'testPadName', 'testDomain')
        except Exception as ex:
            self.assertIsInstance(ex, ValueError)
            self.assertEqual(str(ex), 'error adding alias.')

    def test_add_sam_to_pad_adds_sam(self):
        post_mock = self.request_mock.post
        post_mock.return_value = Mock(ok=True, content=encode_response(GET_PAD_RESPONSE))

        self.subject.add_sam_to_pad('testPadName', {'one': 'two'})
        post_mock.assert_called_once_with(
            data={'sessionToken': 'testSessionToken', 'apiKey': 'testApiKey', 'sam_json': {'one': 'two'},
                  'output': 'json'}, url='https://openapi.cdnetworks.com/api/rest/pan/sam/testPadName/add')

    def test_add_sam_raises_exception_on_api_error(self):
        post_mock = self.request_mock.post
        post_mock.return_value = Mock(ok=False, content=encode_response(GET_PAD_RESPONSE))
        post_mock.return_value.raise_for_status.side_effect = RuntimeError('error')

        try:
            self.subject.add_sam_to_pad('testPadName', {'one': 'two'})
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'error')
        post_mock.assert_called_once_with(
            data={'sessionToken': 'testSessionToken', 'apiKey': 'testApiKey', 'sam_json': {'one': 'two'},
                  'output': 'json'}, url='https://openapi.cdnetworks.com/api/rest/pan/sam/testPadName/add')

