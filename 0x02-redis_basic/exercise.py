#!/usr/bin/env python3
"""Module for using redis"""

from typing import Callable, Union
import uuid
import redis
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a
    function in Redis.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The decorated method.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        # Creating keys for input and output lists
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        # Storing input arguments
        self._redis.rpush(input_key, str(args))

        # Executing the wrapped function to get the output
        result = method(self, *args, **kwargs)

        # Storing the output in the Redis list
        self._redis.rpush(output_key, str(result))

        # Returning the output
        return result

    return wrapper


def replay(fn: Callable) -> None:
    """
    Displays the call history of Cache class method.
    """
    if fn is None or not hasattr(fn, '__self__'):
        return
    redis_store = getattr(fn.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis):
        return
    fxn_name = fn.__qualname__
    in_key = '{}:inputs'.format(fxn_name)
    out_key = '{}:outputs'.format(fxn_name)
    fxn_call_count = 0
    if redis_store.exists(fxn_name) != 0:
        fxn_call_count = int(redis_store.get(fxn_name))
    print('{} was called {} times:'.format(fxn_name, fxn_call_count))
    fxn_inputs = redis_store.lrange(in_key, 0, -1)
    fxn_outputs = redis_store.lrange(out_key, 0, -1)
    for fxn_input, fxn_output in zip(fxn_inputs, fxn_outputs):
        print('{}(*{}) -> {}'.format(
            fxn_name,
            fxn_input.decode("utf-8"),
            fxn_output,
        ))


class Cache:
    """Represents an object for storing data in a Redis data storage."""

    def __init__(self):
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable[[bytes], Union[str, int, float]] =
            None) -> Union[str, int, float, bytes, None]:
        """
        Retrieves data from Redis using the provided key and optionally
        applies a conversion function.
        """
        data = self._redis.get(key)
        if data is None:
            return None

        return fn(data) if fn else data

    def get_str(self, key: str) -> Union[str, None]:
        """Retrieves data from Redis as a string."""
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Union[int, None]:
        """Retrieves data from Redis as an integer."""
        return self.get(key, fn=lambda x: int(x))
