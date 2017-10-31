from . import base


class Actions(object):
    def __init__(self, args, session_token, api_key):
        self.args = args
        self.base = base.Base(args)
        self.session_token = session_token
        self.api_key = api_key

    def create_pad(self, contract_number, new_pad_name, origin, description=None):
        self.clone_pad(contract_number, new_pad_name, origin, description)

    def clone_pad(self, contract_number, src_pad_name=None, new_pad_name='www.newPADName.com',
                  origin=None, description=None):
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'pad': new_pad_name,
            'product': contract_number,
            'output'	: self.base.APIFORMAT
        }
        if src_pad_name:
            params['copy_settings_from'] = src_pad_name
        if origin:
            params['origin'] = origin
        if description:
            params['description'] = description
        return self.base.execute('pan/site/v2/add', params)

    def add_alias_to_pad(self, pad, pad_name, domain):
        existing_aliases = pad['PadConfigResponse']['data']['data']['pad_aliases'].split("\n")
        existing_aliases.append(domain)
        existing_aliases = list(set(existing_aliases))
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'pad': pad_name,
            'pad_aliases': "\n".join(existing_aliases),
            'output': self.base.APIFORMAT
        }
        response = self.base.execute('pan/site/v2/edit', params)
        if response['PadConfigResponse']['resultCode'] == 200:
            pad['PadConfigResponse']['data']['data']['pad_aliases'] = "\n".join(existing_aliases)
        return pad

    def add_sam_to_pad(self, dest_pad_name, rule):
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'sam_json': rule,
            'output': self.base.APIFORMAT}
        return self.base.execute('pan/sam/' + dest_pad_name + '/add', params)
