#!/usr/bin/env python3
"""
This module defines the Cache class for storing data in Redis.
"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count for that key every time
        the method is called
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that records input and output data in Redis lists.
        """
        key = method.__qualname__
        input_key = f"{key}:inputs"
        output_key = f"{key}:outputs"

        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)

        self._redis.rpush(output_key, str(result))
        return result
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls of a particular function.
    """
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    inputs = Cache._redis.lrange(input_key, 0, -1)
    outputs = Cache._redis.lrange(output_key, 0, -1)

    print(f"{key} was called {len(inputs)} times:")

    for input_args, output in zip(inputs, outputs):
        input_args_str = ", ".join(eval(input_args))
        print(f"{key}(*({input_args_str},)) -> {output}")


class Cache:
    """
    Cache class for storing data in Redis.
    """

    def __init__(self):
        """
        Initialize the Cache instance with a Redis client
        and flush the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis with a random key.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieve data from Redis using the provided key.
        """
        data = self._redis.get(key)
        if data is not None and fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """
        Retrieve a string from Redis using the provided key.
        """
        return str(self._redis.get(key))

    def get_int(self, key: str) -> int:
        """
        Retrieve an integer from Redis using the provided key.
        """
        return int(self._redis.get(key))
