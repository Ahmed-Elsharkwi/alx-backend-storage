#!/usr/bin/env python3
"""
create class Cache
"""
from functools import wraps
from typing import Union, Callable, Optional
import uuid
import redis
import json


def count_calls(method: Callable) -> Callable:
    """ count how many times methods of the cache are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ return a function """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ push the inputs keys and the outputs """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ wrapper """
        self._redis.rpush(inputs, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(outputs, result)
        return result
    return wrapper


def replay(method: Callable) -> None:
    """ display the history of calls """
    cache = redis.Redis()
    num = cache.get(method.__qualname__).decode("utf-8")
    print(f"{method.__qualname__} was called {num} times:")
    inputs = cache.lrange("{}:inputs".format(
        method.__qualname__), 0, -1)
    outputs = cache.lrange("{}:outputs".format(
        method.__qualname__), 0, -1)
    for inputs, outputs in zip(inputs, outputs):
        inputs = inputs.decode("utf-8")
        outputs = outputs.decode("utf-8")
        print(f"{method.__qualname__}(*{inputs}) -> {outputs}")


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
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ return string """
        return str(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """ return integer """
        return int(self._redis.get(key))

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        takes a data argument and returns a string.
        The method should generate a random key (e.g. using uuid),
        store the input data in Redis using the random key and return the key.
        """
        random_key = str(uuid.uuid4())
        self._redis.set(random_key, data)
        return random_key
