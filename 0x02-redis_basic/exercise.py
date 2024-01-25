#!/usr/bin/env python3
"""Module for using redis"""

from typing import Union
import uuid
import redis


class Cache:
    """Represents an object for storing data in a Redis data storage."""

    def __init__(self):
        """Initializes a Cache instance."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores a value in a Redis data storage and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
