#!/usr/bin/env python3
""" redis with requests """
import requests
from functools import wraps
from typing import Callable
import redis


def count(method: Callable):
    """ Count the call to requests """
    req = redis.Redis()

    @wraps(method)
    def wrapped(url):
        """ function that will count """
        req.incr(f"count:{url}")
        expiration_count = req.get(f"cached:{url}")
        if expiration_count:
            return expiration_count.decode('utf-8')
        html = method(url)
        req.setex(f"cached:{url}", 10, html)
        return html

    return wrapped


@count
def get_page(url: str) -> str:
    """ module to obtain the HTML """
    return requests.get(url).text
