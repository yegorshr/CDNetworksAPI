from .helper import select_item_by_user, select_from_list


class Browser(object):
    def __init__(self, api_base):
        self.api_base = api_base

    def get_api_key_for_service(self, session_token, svc_name):
        """
        Execute getApiKeyList, search for PAD/service APIKey.
        For new PAD you must to have service where type is 0.
        Unless you need to create new PAD, service Name will be as PAD Name

        Parameters
        ----------
        session_token    : Login token from GetTokenForSelectedControlGroup function.
        svc_name         : Service name


        Returns
        -------
        Error http code or decoded json output
        """
        # In case of implemention action to create new PAD, this login need to be modified
        params = {
            'sessionToken': session_token,
            'output': self.api_base.APIFORMAT
        }

        api_key_list = self.api_base.execute('getApiKeyList', "GET", params)
        service_type = 0
        services = [obj for obj in api_key_list["apiKeyInfo"]["apiKeyInfoItem"] if (obj['type'] == service_type)]

        selected_service = select_from_list(services, svc_name, "Service Name was not found.")
        return selected_service['apiKey']

    def get_token_for_control_group(self, token, svc_group_name):
        """
            Select a control group and return sessionToken
        """
        session_data = select_from_list(token["loginResponse"]["session"], svc_group_name,
                                        "Group Name was not found.", 'svcGroupName', 'sessionToken')
        return session_data['sessionToken']

    def get_pad_list(self, token, api_key):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.api_base.APIFORMAT}
        return self.api_base.execute('pan/site/list', "GET", params)

    def select_pad(self, pads, pad):
        selected_pad = select_from_list(pads["PadConfigResponse"]["data"]["data"], pad,
                                        "PAD Name was not found.", 'pad')
        return selected_pad["pad"]

    def get_pad(self, token, api_key, pad_name, prod=True):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'pad': pad_name,
            'prod': prod,
            'output': self.api_base.APIFORMAT}
        result = self.api_base.execute('pan/site/view', "GET", params)
        if result['PadConfigResponse']["data"]["errors"] != "":
            raise ValueError(result['PadConfigResponse']["data"]["errors"])
        return result

    def get_sam(self, token, api_key, pad_name):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.api_base.APIFORMAT
        }
        return self.api_base.execute('pan/sam/' + pad_name + '/view', "GET", params)

    def get_contract_number(self, token, api_key):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.api_base.APIFORMAT
        }

        contract_list = self.api_base.execute('pan/contract/list', "GET", params)
        choosen_session = select_item_by_user(contract_list['PadConfigResponse']['data']['data'])
        contract_number = contract_list['PadConfigResponse']['data']['data'][choosen_session]['contract_no']
        return contract_number
