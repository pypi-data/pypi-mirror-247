import datetime
import json
import time
from typing import List, Dict

from common_tool.datetime import datetime_to_str
from django.core.serializers.json import DjangoJSONEncoder
from django_redis import get_redis_connection
from functools import wraps
import urllib.parse

from common_tool.function_too import costum_json_decoder


class RedisCli(object):

    def __init__(self):
        self.redis = get_redis_connection()

    def hget(self, name: str, key: str, del_after_get: bool = False) -> str:
        res = self.redis.hget(name=name, key=key)
        if isinstance(res, bytes):
            res = res.decode('utf8')
        if del_after_get and res is not None:
            self.hdel(name=name, key=key)
        if res == 'NaN':
            res = None
        return res

    def hget_json(self, name: str, key: str, del_after_get: bool = False) -> str:
        res = self.redis.hget(name=name, key=key)
        if res:
            res = json.loads(res)
        if del_after_get and res is not None:
            self.hdel(name=name, key=key)
        return res

    def hset(self, name: str, key: str, value: str):
        return self.redis.hset(name, key, value)

    def hdel(self, name: str, key: str):
        return self.redis.hdel(name, key)

    def hkeys(self, name: str) -> List[str]:
        return [k.decode('utf8') for k in self.redis.hkeys(name) if isinstance(k, bytes)]

    def hgetall(self, name: str) -> Dict[str, str]:
        result = dict()
        all_data = self.redis.hgetall(name=name)
        for k, v in all_data.items():
            if isinstance(k, bytes):
                k = k.decode('utf8')
            if isinstance(v, bytes):
                v = v.decode('utf8')
            result[k] = v
        return result

    def get(self, name: str, del_after_get: bool = False, encoding="utf-8") -> str:
        res = self.redis.get(name=name)
        if isinstance(res, bytes):
            res = res.decode(encoding)
        if del_after_get and res:
            self.delete(name=name)
        return res

    def set(self, name: str, value: str, expires_in: int = None):
        return self.redis.set(name=name, value=value, ex=expires_in)

    def delete(self, name: str):
        return self.redis.delete(name)

    def enqueue_data(self, name, data):
        self.redis.rpush(name, str(data))

    def dequeue_data(self, name):
        data = self.redis.lpop(name)
        if data:
            return eval(data)
        return None

    def lrange(self, name):
        data = self.redis.lrange(name, 0, -1)
        return [eval(item) for item in data]

    def publish(self, channel_name, message):
        self.redis.publish(channel_name, message)

    def subscribe(self, channel_name):
        pub = self.redis.pubsub()
        pub.subscribe(channel_name)  # 调频道
        pub.parse_response()  # 准备接收
        return pub


redis_cli = RedisCli()


def build_cache_key(func, *args, **kwargs):
    key_parts = [func.__name__]
    if args:
        args_str = ':'.join([str(arg) for arg in args])
        key_parts.append(f'({args_str})')
    if kwargs:
        kwargs_str = ':'.join([f'{key}={urllib.parse.quote(str(value))}' for key, value in kwargs.items()])
        key_parts.append(f'({kwargs_str})')
    cache_key = ':'.join(key_parts)
    return cache_key


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return datetime_to_str(o)
        return super().default(o)


def func_cache(timeout=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            cache_key = build_cache_key(func, *args, **kwargs)
            result = redis_cli.get(cache_key)
            if not result:
                result = func(*args, **kwargs)
                serialized_result = json.dumps(result, cls=CustomJsonEncoder)
                redis_cli.set(cache_key, serialized_result, timeout)
            else:
                result = json.loads(result, object_hook=costum_json_decoder)
            return result

        return wrapper

    return decorator


def clear_func_cache(func, *args, **kwargs):
    cache_key = build_cache_key(func, *args, **kwargs)
    redis_cli.delete(cache_key)
