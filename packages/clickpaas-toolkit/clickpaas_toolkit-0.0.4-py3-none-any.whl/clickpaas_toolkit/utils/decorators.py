# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     decorators
   Description :
   Author :       yangzhixiang
   date：          2020/9/18
-------------------------------------------------
"""

import inspect
import timeit
import time
from functools import wraps
from collections import OrderedDict


def singleton(cls):
    """
    单例模式装饰器
    :param cls:
    :return:
    """
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


def singleton_with_parameters(cls):
    """
    单例模式装饰器(如果参数一样的话)
    :param cls:
    :return:
    """
    instances = {}

    def _singleton(*args, **kwargs):
        key = frozenset(inspect.getcallargs(cls.__init__, *args, **kwargs).items())
        if key not in instances:
            instances[key] = cls(*args, **kwargs)
        return instances[key]

    return _singleton


class Singleton:
    """单实例元类"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kwargs)
        return cls._instance


class SingletonIfSameParameters(type):
    """
    单实例元类(如果参数一样的话)
    """
    _instances = {}
    _init = {}

    def __int__(cls, name, bases, dct):
        cls._init[cls] = dct.get('__init__', None)

    def __call__(cls, *args, **kwargs):
        init = cls._init[cls]
        if init is not None:
            key = (cls, args, repr(OrderedDict(kwargs.items())))
        else:
            key = cls
        if key not in cls._instances:
            cls._instances[key] = super(SingletonIfSameParameters, cls).__call__(*args, **kwargs)
        return cls._instances[key]


class MaxRetriesExceeded(Exception):
    pass


class InterruptRetry(Exception):
    pass


def retry(exit_condition, interval=1, retries=10, duration=30, interrupt_condition=None):
    """该装饰器可以用于异步业务接口,通过多次调用,确认业务处理完成当重试次数or重试时间,任一条件满足,均会退出重试逻辑,抛出异常
    :param exit_condition: 正常退出条件
    :param interval: 每次等待间隔
    :param retries: 重试次数
    :param duration: 重试时间
    :param interrupt_condition: 异常退出条件，表示exit_condition不可能再有机会满足，中断重试
    :return:
    """

    def wrapper(func):
        @wraps(func)
        def _wrapper(*args, **kwargs):
            n = 0
            start = timeit.default_timer()
            while 1:
                ret = func(*args, **kwargs)
                if not exit_condition(ret):
                    if interrupt_condition is not None and interrupt_condition(ret):
                        raise InterruptRetry("meet the interrupt condition")
                    n += 1
                    if n > retries or timeit.default_timer() - start > duration:
                        raise MaxRetriesExceeded("unexpected result: {}".format(ret))
                    else:
                        time.sleep(interval)
                else:
                    return ret

        return _wrapper

    return wrapper


def cached(func):
    """缓存装饰器,用于function,当传入参数一致,func不会再次执行,而是直接从缓存里取出上次执行结果返回
    :param func:
    :return:
    """
    cached_items = {}

    @wraps(func)
    def wrap(*args, **kwargs):
        key1 = "".join(map(lambda arg: str(id(arg)), args))
        key2 = OrderedDict(sorted({k: id(v) for k, v in kwargs.items()}.items()))
        key = key1 + "+" + str(key2)
        if key in cached_items:
            return cached_items[key]
        else:
            ret = func(*args, **kwargs)
            cached_items[key] = ret
            return ret

    return wrap
