#!/usr/bin/env python3
"""
A web request caching and tracking tool module
"""
import redis
from functools import wraps
import requests

redis_conn = redis.Redis(host='localhost', port=6379, db=0)

# Decorator to cache function result with count and expiration


def cache_with_count(expiration=10):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            url = args[0]  # Assuming the URL is the first argument
            count_key = f"count:{url}"
            cache_key = f"cache:{url}"

            # Increment access count
            redis_conn.incr(count_key)

            # Check if the result is already cached
            cached_result = redis_conn.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            # Call the original function and cache the result
            result = func(*args, **kwargs)
            redis_conn.set(f'count:{url}', 0)
            redis_conn.setex(cache_key, expiration, result)

            return result
        return wrapper
    return decorator


@cache_with_count()
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text
