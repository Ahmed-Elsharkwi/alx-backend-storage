#!/usr/bin/env python3
"""
create class Cache
"""
from typing import Union, Callable, Optional
import uuid
import redis
import json


class Cache:
    """ class Cache """

    def __init__(self) -> None:
        """
        store an instance of the Redis client as a private variable
        named _redis (using redis.Redis()) and
        flush the instance using flushdb
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def get(self, key: str, fn: 
            Optional[callable] = None) -> Union[str, bytes, int, float]:
        """ get the desired data """
        data = self._redis.get(key)
        if fn != None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ return string """
        return str(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """ return integer """
        return int(self._redis.get(key))

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
