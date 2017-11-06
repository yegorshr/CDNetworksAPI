import unittest
from cdnetworks import Base, Browser
from unittest.mock import patch, Mock, call
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

PADS = {"PadConfigResponse": {
    "data": {
        "data": [
            {'origin': 'origin1.fqdn.com', 'pad': 'pad1.cdnet.com', 'id': 1},
            {'origin': 'origin2.fqdn.com', 'pad': 'origin2.cdnet.com', 'id': 2}]
    }}}

GET_PAD_RESPONSE = {
    "PadConfigResponse": {
        'resultCode': 200,
        'data': {
            'errors': '',
            'data': {
                'origin_failure_redirect_url': '',
                'rewrite_rules_post_validation': '',
                'use_origin_multiple_dns_record': False,
                'tag_time_allowed_sec': 0,
                'accept_setting_from_query_string': True,
                'pdseek_flv_extensions': '',
                'honor_path_range': False,
                'misc_comment': '',
                'http_auth_password': '',
                'use_sub_files': True,
                'max_age_rules': '', 'enable_ssl': True,
                'rps_peak': '1 - 2,500',
                'http_auth_type': 'Basic',
                'max_requests_per_keep_alive': 0,
                'tag_hash_format_preset': 0,
                'full_url_rewrite_rules': '',
                'files_type': 'jpg',
                'origin_host_header': '',
                'force_not_modified_on_ims': 0,
                'nam_percent': -1,
                'failed_referrer_check_redirect_url': '',
                'origin_ip': '', 'cookie_exchange': False,
                'use_pad_as_host_header': False,
                'description': '',
                'backup_origin': '',
                'pdseek_default_type': 'flv',
                'http_auth_user': '',
                'force_maxage_on_40x': 0,
                'referrer_list': '',
                'gzip_compression': True,
                'files_size_avg': -1,
                'default_last_modified_date': '',
                'drop_precise_params_in_cache_url': '',
                'url_test': 'test-object.htm',
                'drop_params': False,
                'progressive_dl_param': '',
                'pass_thru_headers_to_origin': '',
                'bypass_empty_referrer_check': True,
                'drop_params_in_cache_url': False,
                'default_max_age': 0,
                'origin': 'suite1.emarsys.net',
                'tag_hash_format': '',
                'tag_check_enabled': False,
                'bps_streaming_limit': 0,
                'tag_time_param': '',
                'files_count': -1,
                'case_insensitive_urls': False,
                'pdseek_h264_extensions': '',
                'tag_time_in_hex': True,
                'drop_params_post_validation': False,
                'reverse_proxy_redirect': True,
                'pass_thru_headers_to_user': '',
                'strict_nocache_support': False,
                'tag_secret': '', 'custom_headers': '',
                'rps_avg': '1 - 2,500',
                'self_implementable': True,
                'honor_byte_range': True,
                'content_variation_rules': '',
                'pad_aliases': 'alias1.url.com',
                'files_size_max': '10-50 MB',
                'drop_precise_params_post_validation': '',
                'referrer_list_type': 'Blacklist',
                'tag_skip_patterns': '',
                'honor_multi_byte_range': False,
                'use_origin_sticky': False,
                'emea_percent': -1,
                'validation_default_redirect_url': '',
                'upstream_ssl': 'Insecure',
                'apac_percent': -1,
                'progressive_dl': False,
                'validation_custom_headers': '',
                'validation_scheme': 'None',
                'status': True,
                'follow_redirect': False,
                'product': '123', 'rewrite_rules': '',
                'mbps_peak': '1-20 Mbps', 'min_age': 0,
                'bypass_validation_on_failure': False,
                'origin_port': 0, 'tag_time_offset_sec': 0,
                'validation_nobypass_redirect_url': '',
                'mbps_avg': '1-20 Mbps',
                'tag_hash_param': '',
                'deny_direct_user_request': False,
                'deploy_status': 'New',
                'buffer_secs': -1}}}}

PAD_NOT_FOUND_RESPONSE = {
    'PadConfigResponse': {'resultCode': 400, 'data': {'errors': 'Invalid PAD supplied.', 'data': {}}}}

RESPONSE_SAM_OK = {
    'PadConfigResponse': {
        'data': {
            'data': {
                'details': [{
                                'do': [{
                                           'mode': '1',
                                           'value': '%{_CLIENT_IP_}',
                                           'id': 'RHO',
                                           'on': 'URQ',
                                           'h': 'X-Aw37jFfq32eh'}],
                                'proc': '1',
                                'name': 'End User IP'}, {
                                'do': [{
                                           'mode': '1',
                                           'value': '%{_CLIENT_IP_}',
                                           'id': 'RHO',
                                           'on': 'URQ',
                                           'h': 'X-Forwarded-For'}],
                                'proc': '1',
                                'name': 'End User Ip in X-Forwarded-For'}]},
            'errors': ''},
        'resultCode': 200}}

RESPONSE_SAM_FAILED = {
    'PadConfigResponse': {
        'resultCode': 400,
        'data': {'errors': 'You can`t view sam rule on this pad(non_existent_pad).', 'data': {}}}}


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

        self.subject.get_sam('session_token', 'test_key', 'pad_name')

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
