import core.network as network
import logging
import time


class BadRequest(Exception):
    pass


class APICode:
    NOT_ENOUGH_PARAMETERS = 0
    SECRET_KEY_NOT_EXISTS = 1
    OK = 2
    RIG_NEED_REGISTER = 3
    BAD_PARAMETER = 4


class Protocol:

    API_ENDPOINTS = {
        'register': {'method': 'GET'}
    }

    def __init__(self, server_host, secret_key):
        self.server_host = server_host
        self.secret_key = secret_key

    def _api_call(self, method, payload):
        payload['key'] = self.secret_key # adding secret key to every request
        endpoint = self.server_host + '/protocol/' + method
        try:
            req = network.make_request(endpoint, self.API_ENDPOINTS[method]['method'], payload)
        except network.NoInternetConnection:
            logging.error('Internet connection lost. Sleeping 60 sec')
            time.sleep(60)
            return self._api_call(method, payload)
        return req.json()

    """
        Retrieves rig configuration and returns it
        Return -1 on fail
    """
    def register_rig(self, observer_version, os, mac):
        payload = {'o_ver': observer_version, 'os': os, 'mac': mac}
        data = self._api_call('register', payload)
        if data['code'] != APICode.OK:
            if data['code'] == APICode.SECRET_KEY_NOT_EXISTS:
                logging.error('Secret key invalid')
                return -1
            else:
                logging.error('API Error: ' + str(data['code']))
                return -1
        return data['data']


