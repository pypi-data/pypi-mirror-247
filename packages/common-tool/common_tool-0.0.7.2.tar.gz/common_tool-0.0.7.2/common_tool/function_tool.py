#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2023/4/4 1:08 PM
# @Author  : donghao
import re
from random import randint
import datetime
import decimal
import uuid
from random import choices
from string import ascii_lowercase, digits

from common_tool.datetime import datetime_to_str


def generate_out_trade_no() -> str:
    """

    :rtype: object
    """
    out_trade_no = f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")}'
    return out_trade_no


def generate_random_str(letter: bool = True, number: bool = True, length: int = 16) -> str:
    population = f'{ascii_lowercase if letter else ""}{digits if number else ""}'
    return ''.join(choices(population, k=length))


def print_log(*args, **kwargs):
    print(f'[{datetime_to_str(datetime.datetime.now())}] {args} {kwargs}')


def random_int(max_value=2147483647):
    return randint(0, max_value)


def random_unsigned_small_int():
    return random_int(65535)


class Singleton(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


PHONE_RE = re.compile('^1[3-9]\d{9}$')


def get_checked_car_plate(plate):
    if not plate:
        return None
    plate = plate.strip().upper()
    if CAR_PLATE_RE.match(plate):
        return plate
    return None


def get_checked_phone(phone):
    if not phone:
        return None
    phone = phone.strip()
    if PHONE_RE.match(phone):
        return phone
    return None


def costum_json_decoder(dct):
    for key, value in dct.items():
        if isinstance(value, str):
            # Check for datetime strings
            if ":" in value:
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f%z")
                except ValueError:
                    try:
                        value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S%z")
                    except ValueError:
                        try:
                            value = datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M%z")
                        except ValueError:
                            pass
            # Check for date strings
            elif "-" in value:
                try:
                    value = datetime.datetime.strptime(value, "%Y-%m-%d").date()
                except ValueError:
                    pass
            # Check for time strings
            elif ":" in value:
                try:
                    value = datetime.datetime.strptime(value, "%H:%M:%S.%f").time()
                except ValueError:
                    try:
                        value = datetime.datetime.strptime(value, "%H:%M:%S").time()
                    except ValueError:
                        pass
            # Check for Decimal strings
            elif value.isdigit():
                value = decimal.Decimal(value)
            # Check for UUID strings
            elif len(value) == 36:
                try:
                    value = uuid.UUID(value)
                except ValueError:
                    pass
        dct[key] = value
    return dct


def query_dict_to_dict(query_dict, with_empty=False):
    """
    将QueryDict转化成dict，request.GET, request.POST转化成dict
    :param query_dict:
    :param with_empty: 结果包含空值参数
    :rtype: dict[str, str]
    """
    result = {k: v for k, v in query_dict.items() if with_empty or len(v) > 0}
    return result
