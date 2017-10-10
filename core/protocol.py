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

    def __init__(self, server_host, secret_key):
        self.server_host = server_host
        self.secret_key = secret_key

    def _api_call(self, method, request_method, payload, return_request=False):
        payload['key'] = self.secret_key  # adding secret key to every request
        endpoint = self.server_host + '/protocol/' + method
        try:
            req = network.make_request(endpoint, request_method, payload)
        except network.NoInternetConnection:
            logging.error('Internet connection lost. Sleeping 60 sec')
            time.sleep(60)
            return self._api_call(method, request_method, payload, return_request)

        if return_request:
            return req
        else:
            return req.json()

    """
        Retrieves rig configuration and returns it
        Return -1 on fail
    """
    def register_rig(self, observer_version, os, mac):
        payload = {'o_ver': observer_version, 'os': os, 'mac': mac}
        data = self._api_call('register', 'get', payload)
        if data['code'] != APICode.OK:
            if data['code'] == APICode.SECRET_KEY_NOT_EXISTS:
                logging.error('Secret key invalid')
                return -1
            else:
                logging.error('API Error: ' + str(data['code']))
                return -1
        return data['data']

    """
        Returns binary content of requested miner (ZIP)
    """
    def get_miner_file(self, miner_type):
        data = self._api_call('miner/' + miner_type, 'get', {}, True).content
        return data



