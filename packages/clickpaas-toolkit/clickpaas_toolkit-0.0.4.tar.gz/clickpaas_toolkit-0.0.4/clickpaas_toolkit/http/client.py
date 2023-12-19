# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     client
   Description :
   Author :       yangzhixiang
   date：          2020/9/17
-------------------------------------------------
"""

import requests
import logging
import timeit
import os
from clickpaas_toolkit.utils.util import Counter, merge_dicts

C = Counter()


def _join_urls(root, *args):
    """
    拼接完整的url
    :param root:
    :param args:
    :return:
    """
    urls = []
    if root.endswith(r"\/"):
        root = root[:-2]
    elif root.endswith("/"):
        root = root[:-1]
    urls.append(root)

    for path in args:
        if path is None or path.strip() == "":
            continue
        if path.startswith(r"\/"):
            path = path[2:]
        elif path.startswith("/"):
            path = path[1:]
        urls.append(path)
    return "/".join(urls)


class BaseClient:
    COOKIE_USER_TAG_KEY = "userTag"

    def __init__(self, base_url, session=None, **kwargs):
        self.base_url = base_url
        if session and not isinstance(session, requests.Session):
            raise TypeError("invalid type of requests.Session")
        self.session = session
        self.response_handlers = []
        self.json_handlers = []
        self.interceptor = None
        self.logger = logging.getLogger(__name__)
        self.req_kwargs = dict(timeout=90)
        self.req_kwargs.update(kwargs)
        self.user_tag = os.environ.get("USER_TAG")
        self._injector = dict()

    def _call_api(self, endpoint, method="post", req_kwargs=None, is_json_resp=True, interceptor=None,
                  disable_log=False):
        """
        http 调用函数
        :param endpoint: 请求地址
        :param method: 请求方法
        :param req_kwargs: 请求参数
        :param is_json_resp: 是否是json返回
        :param interceptor: 拦截器，可修改返回值
        :param disable_log: 是否关闭打印日志，默认开启，如果是上传图片建议关闭
        :return:
        """
        url = _join_urls(self.base_url, endpoint)
        req_id = C.counter
        kwargs = self.req_kwargs.copy()
        merge_dicts(kwargs, req_kwargs)

        if not self.session:
            self.session = requests.session()
        if self.user_tag:
            self.session.cookies[BaseClient.COOKIE_USER_TAG_KEY] = self.user_tag
        if not disable_log:
            self.logger.info("start request", extra=dict(url=url, method=method, parameters=kwargs, request_oid=req_id,
                                                         cookie=self.session.cookies.get_dict()))
        start = timeit.default_timer()
        response = self.session.request(method, url, **kwargs)
        if not disable_log:
            self.logger.info("got response", extra=dict(response=response.text, request_id=req_id, url=response.url,
                                                        is_json_format=is_json_resp, status_code=response.status_code,
                                                        latency=int((timeit.default_timer() - start) * 1000)))
        for handler in self.response_handlers:
            handler(response)
        response.raise_for_status()
        if is_json_resp:
            try:
                response_to_json = response.json()
            except ValueError:
                if not disable_log:
                    self.logger.error("failed to convert to json response", extra=dict(request_id=req_id))
                raise
            else:
                for handler in self.json_handlers:
                    handler(response_to_json)
        interceptor_fun = interceptor or self.interceptor
        return response if interceptor_fun is None else interceptor_fun(response,
                                                                        locals().get('response_to_json', None))
