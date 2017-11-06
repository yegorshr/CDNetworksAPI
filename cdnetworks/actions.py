class Actions(object):
    def __init__(self, api_base, session_token, api_key):
        self.api_base = api_base
        self.session_token = session_token
        self.api_key = api_key

    def clone_pad(self, contract_number, src_pad_name, new_pad_name, origin, description=None):
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'pad': new_pad_name,
            'product': contract_number,
            'output'	: self.api_base.APIFORMAT
        }
        if src_pad_name:
            params['copy_settings_from'] = src_pad_name
        if origin:
            params['origin'] = origin
        if description:
            params['description'] = description
        return self.api_base.execute('pan/site/v2/add', "POST", params)

    def add_alias_to_pad(self, pad, pad_name, domain):
        existing_aliases = pad['PadConfigResponse']['data']['data']['pad_aliases'].split("\n")
        existing_aliases.append(domain)
        existing_aliases = sorted(set(existing_aliases))
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'pad': pad_name,
            'pad_aliases': "\n".join(existing_aliases),
            'output': self.api_base.APIFORMAT
        }
        response = self.api_base.execute('pan/site/v2/edit', "POST", params)
        if response['PadConfigResponse']['resultCode'] == 200:
            pad['PadConfigResponse']['data']['data']['pad_aliases'] = "\n".join(existing_aliases)
        else:
            raise ValueError(response['PadConfigResponse']['data']['errors']['general'])
        return pad

    def add_sam_to_pad(self, dest_pad_name, rule):
        params = {
            'sessionToken': self.session_token,
            'apiKey': self.api_key,
            'sam_json': rule,
            'output': self.api_base.APIFORMAT}
        return self.api_base.execute('pan/sam/' + dest_pad_name + '/add', "POST", params)
