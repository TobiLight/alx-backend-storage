#!/usr/bin/env python3
"""
A web request caching and tracking tool module
"""
from typing import Callable
import redis
from functools import wraps
import requests


redis_conn = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    '''Caches the output of fetched data.
    '''
    @wraps(method)
    def invoker(url) -> str:
        '''The wrapper function for caching the output.
        '''
        redis_conn.incr(f'count:{url}')
        result = redis_conn.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_conn.set(f'count:{url}', 0)
        redis_conn.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    '''Returns the content of a URL after caching the request's response,
    and tracking the request.
    '''
    return requests.get(url).text
