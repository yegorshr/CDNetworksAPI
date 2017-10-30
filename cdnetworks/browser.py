from .base import Base
from .helper import select_item_by_user, select_from_list


class Browser(object):
    def __init__(self, args):
        self.args = args
        self.base = Base(args)

    def get_api_key_for_pad(self, session_token):
        """
        Execute getApiKeyList, search for PAD/service APIKey.
        For new PAD you must to have service where type is 0.
        Unless you need to create new PAD, service Name will be as PAD Name

        Parameters
        ----------
        session_token    : Login token from GetTokenForSelectedControlGroup function.

        Returns
        -------
        Error http code or decoded json output
        """
        # In case of implemention action to create new PAD, this login need to be modified
        params = {
            'sessionToken': session_token,
            'output': self.base.APIFORMAT
        }

        api_key_list = self.base.execute('getApiKeyList', params)
        service_type = 0
        services = [obj for obj in api_key_list["apiKeyInfo"]["apiKeyInfoItem"] if (obj['type'] == service_type)]

        selected_service = select_from_list(services, self.args.svc_name, "Service Name was not found.")
        return selected_service['apiKey']

    def get_token_for_control_group(self, token):
        """
            Select a control group and return sessionToken
        """
        session_data = select_from_list(token["loginResponse"]["session"], self.args.svc_group_name,
                                        "Group Name was not found.", 'svcGroupName', 'sessionToken')
        return session_data['sessionToken']

    def get_pad_list(self, token, api_key):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.base.APIFORMAT}
        return self.base.execute('pan/site/list', params)

    def select_pad(self, pads):
        selected_pad = select_from_list(pads["PadConfigResponse"]["data"]["data"], self.args.src_pad_name,
                                        "PAD Name was not found.", 'pad')
        return selected_pad["pad"]

    def get_pad(self, token, api_key, pad_name, prod=True):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'pad': pad_name,
            'prod': prod,
            'output': self.base.APIFORMAT}
        return self.base.execute('pan/site/view', params)

    def get_sam(self, token, api_key, pad_name):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.base.APIFORMAT
        }
        return self.base.execute('pan/sam/' + pad_name + '/view', params)

    def get_contract_number(self, token, api_key):
        params = {
            'sessionToken': token,
            'apiKey': api_key,
            'output': self.base.APIFORMAT
        }

        contract_list = self.base.execute('pan/contract/list', params)
        choosen_session = select_item_by_user(contract_list['PadConfigResponse']['data']['data'])
        contract_number = contract_list['PadConfigResponse']['data']['data'][choosen_session]['contract_no']
        return contract_number
