#!/usr/bin/env python3
"""module for Implementing an expiring web cache and tracker"""

import requests
import redis
from functools import wraps
from typing import Callable

# Initialize Redis client
redis_client = redis.Redis()


def cache_page(func: Callable) -> Callable:
    """
    Decorator to cache the result of a function with an expiration time.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = args[0]
        cache_key = f"cache:{url}"
        count_key = f"count:{url}"

        cached_result = redis_client.get(cache_key)
        if cached_result:
            redis_client.incr(count_key)
            return cached_result.decode('utf-8')

        result = func(*args, **kwargs)

        redis_client.setex(cache_key, 10, result)

        redis_client.incr(count_key)

        return result

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Retrieve the HTML content of a given URL.
    """
    response = requests.get(url)
    return response.text
