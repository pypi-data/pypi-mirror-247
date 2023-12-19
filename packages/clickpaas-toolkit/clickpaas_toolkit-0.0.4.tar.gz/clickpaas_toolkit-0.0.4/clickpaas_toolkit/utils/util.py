# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     util
   Description :
   Author :       yangzhixiang
   date：          2020/9/17
-------------------------------------------------
"""

import hashlib
import random
import string
import threading


class Bunch(dict):
    """
    >>> d = dict(name="test", age=16, data={"cellphone": 123456})
    >>> b = Bunch(d)
    >>> b.name == d["name"] # True
    >>> b.data.cellphone == 123456 # True
    >>> b.name = "666"
    >>> b.name == "666" # True
    """

    def bunch_nest(self, x):
        if isinstance(x, dict):
            return Bunch((k, self.bunch_nest(v)) for k, v in x.items())
        elif isinstance(x, (list, tuple)):
            return type(x)(self.bunch_nest(v) for v in x)
        else:
            return x

    def __init__(self, obj) -> None:
        super().__init__()
        super(Bunch, self).update(self.bunch_nest(obj))

    def __getattr__(self, item):
        try:
            object.__getattribute__(self, item)
        except AttributeError:
            try:
                value = super(Bunch, self).__getitem__(item)
            except KeyError as e:
                raise AttributeError("attribute: {} not found".format(item)) from e
            else:
                if isinstance(value, dict):
                    return Bunch(value)
                return value

    def __setattr__(self, key, value):
        super(Bunch, self).__setitem__(key, value)


def md5_str(content: str, encoding='utf8') -> str:
    """
    计算字符串md5
    :param content: 需要md5内容
    :param encoding: 编码方式
    :return:
    """
    m = hashlib.md5(content.encode(encoding))
    return m.hexdigest()


def md5_file(file_path, block=1024):
    """
    计算文件md5
    :param file_path: 文件路径
    :param block: 读取块大小
    :return:
    """
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            c = f.read(block)
            if c:
                m.update(c)
            else:
                break
    return m.hexdigest()


def gen_rand_str(length=8, s_type='hex', prefix=None, postfix=None):
    """生成指定长度的随机数，可设置输出字符串的前缀、后缀字符串

    :param length: 随机字符串长度
    :param s_type:
    :param prefix: 前缀字符串
    :param postfix: 后缀字符串
    :return:
    """
    if s_type == 'digit':
        formatter = "{:0" + str(length) + "}"
        mid = formatter.format(random.randrange(10 ** length))
    elif s_type == 'ascii':
        mid = "".join([random.choice(string.ascii_letters) for _ in range(length)])
    elif s_type == "hex":
        formatter = "{:0" + str(length) + "x}"
        mid = formatter.format(random.randrange(16 ** length))
    else:
        mid = "".join([random.choice(string.ascii_letters + string.digits) for _ in range(length)])

    if prefix is not None:
        mid = prefix + mid
    if postfix is not None:
        mid = mid + postfix
    return mid


def low_case_to_camelcase(arg_name):
    """
    category_id -> categoryId
    :param arg_name: 参数
    :return:
    """
    args = arg_name.split("_")
    return args[0] + "".join([a.capitalize() for a in args[1:]])


def camelcase_to_low_case(arg_name):
    """
    categoryId -> category_id
    :param arg_name: 参数
    :return:
    """
    args = ""
    for i in range(0, len(arg_name)):
        if arg_name[i].isupper():
            args += '_'
            args += arg_name[i].lower()
        else:
            args += arg_name[i]
    return args


class Counter(object):
    """
    计数器
    """

    def __init__(self, start=0):
        self._counter = start
        self.lock = threading.RLock()

    @property
    def counter(self):
        self.lock.acquire()
        self._counter += 1
        ret = self._counter
        self.lock.release()
        return ret

    @property
    def current(self):
        self.lock.acquire()
        ret = self._counter
        self.lock.release()
        return ret


def merge_dicts(d1, d2):
    """
    dict合并，
    :param d1:
    :param d2:
    :return:
    """
    if d1 is None:
        return d2
    if d2 is None:
        return d1
    common_keys = set(d1.keys()) & set(d2.keys())
    for k in common_keys:
        if isinstance(d1[k], dict) and isinstance(d2[k], dict):
            d2[k] = merge_dicts(d1[k], d2[k])
    d1.update(d2)
    return d1


def avoid_buildin_keywords(param, prefix):
    """变量名、参数名请勿使用id/type，与内置关键字冲突"""
    keys = ("id", "type")
    for key in keys:
        if param == "{}_{}".format(prefix, key):
            return key
    return param


def avoid_buildin_keywords_low_case_to_camelcase(param, prefix):
    """变量名、参数名请勿使用id/type，与内置关键字冲突  and category_id -> categoryId"""
    param = avoid_buildin_keywords(param, prefix)
    return low_case_to_camelcase(param)


