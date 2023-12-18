# Copyright 2014 Flyme, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module provides authentication functions for fce services.
"""
from __future__ import absolute_import

import datetime
import time
from builtins import str
from builtins import bytes
import hashlib
import hmac
import logging

from flymefce.http import http_headers
from flymefce import utils
from flymefce import FLYME_YUN_VERSION, FLYME_SIGN_ALG


_logger = logging.getLogger(__name__)


def _get_canonical_headers(headers, headers_to_sign=None):
    headers = headers or {}

    if headers_to_sign is None or len(headers_to_sign) == 0:
        headers_to_sign = {b"host", b"content-md5", b"content-length", b"content-type"}

    result = []
    for k in headers:
        k_lower = k.strip().lower()
        value = utils.convert_to_standard_string(headers[k]).strip()
        if k_lower.startswith(http_headers.FCE_PREFIX) or k_lower in headers_to_sign:
            str_tmp = b"%s:%s" % (utils.normalize_string(k_lower), utils.normalize_string(value))
            result.append(str_tmp)

    result.sort()
    return b'\n'.join(result)


def sign(credentials,
         http_method,
         path,
         headers,
         params,
         timestamp=0,
         expiration_in_seconds=1800,
         headers_to_sign=None,
         nonce=None):
    """
    请求Flyme云网关业务加签

    Args:
        credentials: FceCredentials: 保存AK/SK的对象
        http_method: str: 请求方法
        path: str: 请求路径
        headers: dict: 请求头
        params: dict: 请求参数
        timestamp: int: 请求时间戳
        expiration_in_seconds: int: 过期时间（单位秒）
        headers_to_sign: set: 需要sign的请求头
        nonce: str: 随机字符串
    Returns:
        sign_result: bytes: 验签字符串
        params: 增加验签后的请求参数
    """
    _logger.debug('Sign params: %s %s %s %s %d %d %s' % (
        http_method, path, headers, params, timestamp, expiration_in_seconds, headers_to_sign
    ))

    if not timestamp:
        timestamp = int(time.time() * 1000)

    ak = credentials.access_key_id
    sk = credentials.secret_access_key
    ver = FLYME_YUN_VERSION

    # 将参数中的bytes转换为str
    new_params = {}
    params = params or {}
    for key, value in params.items():
        if isinstance(key, bytes):
            key = key.decode('utf-8')
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        new_params[key] = value
    params = new_params

    params["ak"] = ak
    params["ver"] = ver
    params["alg"] = FLYME_SIGN_ALG
    params["nonce"] = nonce if nonce else utils.random_string(6)
    params["ts"] = str(timestamp)

    canonical_querystring = utils.get_flyme_canonical_querystring(params, True)
    sign_string = sk + canonical_querystring + sk
    sign_result = hashlib.md5(sign_string.encode('utf-8')).hexdigest()

    params["sign"] = sign_result

    return sign_result, params
