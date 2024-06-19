#!/usr/bin/env python3
"""
create class Cache
"""
from typing import Union
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
        self.__redis = redis.Redis()
        self.__redis.flushdb(True)

    def store(self, data: Union[str, bytes, int | float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        random_key = str(uuid.uuid4())
        self.__redis.set(random_key, data)
        return random_key
