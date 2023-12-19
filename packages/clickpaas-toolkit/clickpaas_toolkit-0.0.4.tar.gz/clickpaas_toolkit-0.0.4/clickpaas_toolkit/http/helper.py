# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     helper
   Description :
   Author :       yangzhixiang
   date：          2020/9/17
-------------------------------------------------
"""
import re
from functools import wraps
from inspect import signature

try:
    import simplejson as json
except ImportError:
    import json


def _set_or_update_node(parent: dict, key: str, d: dict):
    if isinstance(parent.get(key, None), dict):
        parent[key].update(d)
    else:
        parent[key] = d


def wrap_payload(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        func(*args, **kwargs)

        parameters = signature(func).parameters
        arguments = list(parameters.keys())
        payload = {parameter.name: parameter.default for _, parameter in parameters.items() if
                   parameter.default is not parameter.empty and parameter.name != "self"}
        if arguments[0] == "self":
            arguments.pop(0)
            args = args[1:]

        if args:
            for index, val in enumerate(args):
                arg_name = arguments[index]
                payload[arg_name] = val

        payload.update(kwargs)
        return payload

    return _wrapper


def api(path, method="post", is_json_req=True, arg_handler=None, remove_none=False, hooks=None, **kwargs):
    """
    restful api 装饰器
    :param path: 接口请求路径, 比如/path/<id>/
    :param method: 请求方法，get/post/put...
    :param is_json_req: 是否是json请求，如果True，则requests.request为json payload
    :param arg_handler: 自定义参数key修正方法，比如将驼峰式参数改为lower_case
    :param remove_none: 是否移除请求参数为None/空字符串的key
    :param hooks: [function(client: BaseClient, method: str, request: requests.request入参)]
    :param kwargs: 具体参考BaseClient._call_api的请求参数
    :return:
    """

    def wrapper(func):
        @wraps(func)
        def _wrapper(self, *fargs, **fkwargs):
            payload = wrap_payload(func)(self, *fargs, **fkwargs)
            # 替换path里面包含<*>的参数，比如/path/<id>
            c = re.compile(r'<\S*?>')
            endpoint = path
            paths = c.findall(endpoint)
            for p in paths:
                tp = p[1:-1]
                if tp not in payload:
                    raise ValueError("invalid restful api format")
                else:
                    endpoint = endpoint.replace(p, str(payload.pop(tp)))
            # 是否移除参数为空的参数
            if remove_none:
                payload = {k: v for k, v in payload.items() if v not in (None, "")}
            # 自定义参数 handler
            if arg_handler:
                payload = {arg_handler(k): v for k, v in payload.items()}

            req_kwargs = kwargs.pop("req_kwargs", {})
            if method.upper() == "GET":
                _set_or_update_node(req_kwargs, 'params', payload)
            elif is_json_req:
                _set_or_update_node(req_kwargs, 'json', payload)
            else:
                _set_or_update_node(req_kwargs, 'data', payload)

            if hooks is not None:
                if callable(hooks):
                    hooks(self, method, req_kwargs)
                else:
                    for hook in hooks:
                        hook(self, method, req_kwargs)
            return self._call_api(endpoint, method, req_kwargs, **kwargs)
        return _wrapper
    return wrapper
