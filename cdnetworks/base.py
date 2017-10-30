import requests
import json
from pprint import pprint


class Base(object):
    def __init__(self, args):
        self.args = args

    API_URL = "https://openapi.cdnetworks.com/api/rest/"  # CDNetworks API url
    APIFORMAT = "json"  # API output format

    def execute(self, endpoint, parameters):
        """
        Execute Rest API

        Parameters
        ----------
        endpoint     : API name Example "login" or "pan/contract/list"
        parameters  : dictionary of paramenter for API

        Returns
        -------
        Error http code or decoded json output
        """
        full_url = self.API_URL + endpoint

        if len(json.dumps(parameters)) > 2000:
            response = requests.post(url=full_url, data=parameters)
        else:
            response = requests.get(url=full_url, params=parameters, verify=True)
        print('Executed url is %s' % response.url) if self.args.verbose else None
        print('Return Code for %s is %s' % (endpoint, response.status_code)) if self.args.verbose else None

        # On success, response code will be 200
        if response.ok:
            # Loading the response data and decode as response not in utf-8 and has digits
            output = json.loads(response.content.decode('utf-8'))
            return output
        else:
            # If response code is not ok (200), print the resulting error
            response.raise_for_status()

    def login(self):
        params = {
            'user': self.args.username,
            'pass': self.args.password,
            'output': self.APIFORMAT}
        output = self.execute('login', params)
        if output['loginResponse']['resultCode'] == 101:
            raise ValueError("User login information is incorrect")
        return output

    def logout(self, token):
        params = {
            'sessionToken': token,
            'output': self.APIFORMAT}
        output = self.execute('logout', params)
        pprint(output) if self.args.verbose else None
