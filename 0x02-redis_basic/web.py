#!/usr/bin/env python3
"""
A web request caching and tracking tool module
"""
from typing import Callable
import redis
from functools import wraps
import requests


redis_conn = redis.Redis()


def data_cacher(func: Callable) -> Callable:
    """Caches the output of a fetched data"""
    @wraps(func)
    def wrapper(url: str) -> str:
        """Wrapper function for caching the output"""
        # Increment access count
        redis_conn.incr(f'count:{url}')

        # Check if the result is already cached
        cached_result = redis_conn.get(f'result:{url}')
        if cached_result:
            return cached_result.decode('utf-8')

        # Call the original function and cache the result
        result = func(url)
        redis_conn.set(f'count:{url}', 0)
        redis_conn.setex(f'result:{url}', 10, result)

        return result
    return wrapper


@data_cacher
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
