import unittest
import cdnetworks
from unittest.mock import patch, Mock
from test.helper_functions import encode_response


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

    def tearDown(self):
        super().tearDown()
        patch.stopall()

    def test_clone_pad_calls_proper_endpoint(self):
        expected_response = {}
        self.request_mock.post.return_value = Mock(ok=True, content=encode_response(expected_response))
        subject = cdnetworks.Actions(self.api_base, 'testSessionToken', 'testApiKey')
        result = subject.clone_pad('testContractNo', 'testSrcPad', 'testNewPad', 'testOrigin', 'testDescription')

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

        subject = cdnetworks.Actions(self.api_base, 'testSessionToken', 'testApiKey')

        try:
            subject.clone_pad('testContract', 'testSrcPad', 'testNewPad', 'testOrigin', 'testDescription')
        except Exception as ex:
            self.assertIsInstance(ex, RuntimeError)
            self.assertEqual(str(ex), 'error')
