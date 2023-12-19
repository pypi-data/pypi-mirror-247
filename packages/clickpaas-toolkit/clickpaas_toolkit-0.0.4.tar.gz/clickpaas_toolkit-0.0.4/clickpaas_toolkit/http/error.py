# -*- coding: utf-8 -*-

"""
-------------------------------------------------
   File Name：     error
   Description :
   Author :       yangzhixiang
   date：          2020/9/17
-------------------------------------------------
"""


class ParserError(Exception):
    pass


class InvalidRequestError(Exception):
    pass


class MethodNotFound(Exception):
    pass


class InvalidParamsError(Exception):
    pass


class InternalError(Exception):
    pass


class ServerError(Exception):
    pass


class ClientError(Exception):
    pass


class ResponseError(Exception):
    pass
