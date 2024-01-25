#!/usr/bin/env python3
"""
A web request caching and tracking tool module
"""
from typing import Callable
import redis
from functools import wraps
import requests

redis_conn = redis.Redis(host='localhost', port=6379, db=0)


def cache_with_count(func: Callable, expiration=10) -> Callable:
    """Caches the output of a fetched data"""
    @wraps(func)
    def wrapper(url: str):
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
        redis_conn.setex(f'result:{url}', expiration, result)

        return result
    return wrapper


@cache_with_count()
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response,
    and tracking the request.
    """
    response = requests.get(url)
    return response.text
