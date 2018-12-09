# -*- coding: utf-8 -*-
from requests.exceptions import HTTPError, ConnectionError


def request_wrapper(req_function, args=[], vars={}):
    """req_function must return a <class 'requests.models.Response'>
       ex.: 
       def req_function():
           return resquests.post(...)
    """
    try:
        response = req_function(*args, **vars)
        response.raise_for_status()
    except HTTPError as err:
        return dict(error=err, response=response)
    except ConnectionError as err:
        return dict(error=err, response=None)
    else:
        return dict(error=None, response=response)
