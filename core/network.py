import requests
import logging
import time


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


def make_waiting_request(url, method='GET', payload=None):
    try:
        req = make_request(url, method, payload)
    except NoInternetConnection:
        logging.error('Internet connection lost. Sleeping 60 sec')
        time.sleep(60)
        return make_waiting_request(url, method, payload)
    return req
