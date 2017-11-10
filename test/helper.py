import json


def encode_response(expected_data):
    return json.dumps(expected_data).encode('utf-8')


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
CONTRACT_RESPONSE = {'PadConfigResponse':
                         {'resultCode': 200,
                          'data':
                              {'errors': '',
                               'data': [
                                   {'status': 'active',
                                    'contract_name': 'CA',
                                    'available_shield_locations': [],
                                    'is_ssl': 0,
                                    'self_implementable': 1, 'is_dwa': 0, 'service_category': 'CA',
                                    'contract_no': '123123'}]}}}
CONTRACT_RESPONSE_ERROR = {'PadConfigResponse':
                               {'resultCode': 200,
                                'data':
                                    {'errors': 'error'}
                                }
                           }

ADD_PAD_ALIAS_FAILED_RESPONSE = {
    'PadConfigResponse': {
        'resultCode': 400,
        'data': {'errors': {'general': 'error adding alias.', 'data': {}}}}}

EMPTY_PAD = {
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
                'pad_aliases': '',
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

PUSH_RESPONSE = {'PadConfigResponse': {'data': {'data': {'details': 'You have requested to push the PAD'
                                                                    ' configuration to our staging servers. '
                                                                    'Please wait a few mins, as the '
                                                                    ' push is in progress.'},
                                                'errors': ''},
                                       'resultCode': 200}
                 }

STATUS_RESPONSE = {'PadConfigResponse': {'data': {'data': {'comment': 'Validating PAD '
                                                                      'configuration. The PAD is '
                                                                      'not editable until the '
                                                                      'job is done.',
                                                           'deploy_status': 'Pushing to Staging',
                                                           'error_message': '',
                                                           'pad': 'testPadName',
                                                           'push_completion_rate': '0',
                                                           'test_nodes': []},
                                                  'errors': ''},
                                         'resultCode': 200}}
