import requests
import json
from pprint import pprint


class Base(object):
    API_URL = "https://openapi.cdnetworks.com/api/rest/"  # CDNetworks API url
    APIFORMAT = "json"  # API output format

    def __init__(self, username, password, verbose=False):
        self.username = username
        self.password = password
        self.verbose = verbose

    def execute(self, endpoint, method, parameters):
        """
        Execute Rest API

        Parameters
        ----------
        endpoint    : API name Example "login" or "pan/contract/list"
        method      : HTTP method : GET or POST
        parameters  : dictionary of paramenter for API

        Returns
        -------
        Error http code or decoded json output
        """
        full_url = self.API_URL + endpoint

        if method == "POST":
            response = requests.post(url=full_url, data=parameters)
        else:
            response = requests.get(url=full_url, params=parameters, verify=True)
        print('Executed url is %s' % response.url) if self.verbose else None
        print('Return Code for %s is %s' % (endpoint, response.status_code)) if self.verbose else None

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
            'user': self.username,
            'pass': self.password,
            'output': self.APIFORMAT}
        output = self.execute('login', "POST", params)
        if output['loginResponse']['resultCode'] == 101:
            raise ValueError("User login information is incorrect")
        return output

    def logout(self, token):
        params = {
            'sessionToken': token,
            'output': self.APIFORMAT}
        output = self.execute('logout', "GET", params)
        pprint(output) if self.verbose else None
