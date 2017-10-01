import requests


class NoInternetConnection(Exception):
    pass


def make_request(url, method='GET', payload=None):
    if payload is None:
        payload = {}
    try:
        if method.lower() == 'get':
            req = requests.get(url, params=payload)
        else:
            req = requests.post(url, data=payload)
    except requests.exceptions.RequestException as e:
        raise NoInternetConnection
    return req
