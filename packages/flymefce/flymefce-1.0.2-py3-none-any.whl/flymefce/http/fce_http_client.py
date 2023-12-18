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
This module provide http request function for fce services.
"""
import json
import uuid

from future.utils import iteritems, iterkeys, itervalues
from builtins import str, bytes
import logging
import http.client
import sys
import time
import traceback

import flymefce
from flymefce import compat
from flymefce import utils
from flymefce.fce_response import FceResponse
from flymefce.exception import FceHttpClientError
from flymefce.exception import FceClientError
from flymefce.http import http_headers, http_content_types

_logger = logging.getLogger(__name__)


def _get_connection(protocol, host, port, connection_timeout_in_millis):
    """
    :param protocol
    :type protocol: flymefce.protocol.Protocol

    :param connection_timeout_in_millis
    :type connection_timeout_in_millis int
    """
    host = compat.convert_to_string(host)
    if protocol.name == flymefce.protocol.HTTP.name:
        return http.client.HTTPConnection(
            host=host, port=port, timeout=connection_timeout_in_millis / 1000)
    elif protocol.name == flymefce.protocol.HTTPS.name:
        return http.client.HTTPSConnection(
            host=host, port=port, timeout=connection_timeout_in_millis / 1000)
    else:
        raise ValueError(
            'Invalid protocol: %s, either HTTP or HTTPS is expected.' % protocol)


def _send_http_request(conn, http_method, uri, headers, body, send_buf_size):
    # putrequest() need that http_method and uri is Ascii on Py2 and unicode \
    # on Py3
    if isinstance(http_method, bytes):
        http_method = http_method.decode('utf-8')
    if isinstance(uri, bytes):
        uri = uri.decode('utf-8')

    conn.putrequest(http_method, uri, skip_host=True, skip_accept_encoding=True)

    for k, v in iteritems(headers):
        if isinstance(v, bytes):
            v = v.decode('utf-8')
        if isinstance(k, bytes):
            k = k.decode('utf-8')
        conn.putheader(str(k), str(v))
    conn.endheaders()

    if body:
        if isinstance(body, (bytes, str)):
            conn.send(body)
        else:
            total = int(headers[http_headers.CONTENT_LENGTH])
            sent = 0
            while sent < total:
                size = total - sent
                if size > send_buf_size:
                    size = send_buf_size
                buf = body.read(size)
                if not buf:
                    raise FceClientError(
                        'Insufficient data, only %d bytes available while %s is %d' % (
                            sent, http_headers.CONTENT_LENGTH, total))
                conn.send(buf)
                sent += len(buf)

    return conn.getresponse()


def check_headers(headers):
    """
    check value in headers, if \n in value, raise
    :param headers:
    :return:
    """
    for k, v in iteritems(headers):
        if isinstance(v, (bytes, str)) and b'\n' in compat.convert_to_bytes(v):
            raise FceClientError(r'There should not be any "\n" in header[%s]:%s' % (k, v))


def send_request(config,
                 sign_function,
                 response_handler_functions,
                 http_method,
                 path,
                 body,
                 headers,
                 params,
                 use_backup_endpoint=False):
    """
    Send request to FlymeYun OpenAPI services.

    Args:
        config: flymefce.FceClientConfiguration: http客户端配置
        sign_function: 加签函数
        response_handler_functions: list: 响应处理函数列表
        http_method: 请求方法
        path: 请求路径
        body: 请求Body
        headers: 请求头
        params: 请求参数
        use_backup_endpoint: bool: 是否使用备份Endpoint

    Returns:
        flymefce.FceResponse
    """
    _logger.debug(b'%s request start: %s %s, %s, %s', http_method, path, headers, params, body)
    headers = headers or {}

    request_endpoint = config.endpoint
    if use_backup_endpoint:
        request_endpoint = config.backup_endpoint

    # 设置请求头 - Host
    headers[http_headers.HOST] = request_endpoint

    should_get_new_date = False
    if http_headers.DATE not in headers or http_headers.FCE_DATE not in headers:
        should_get_new_date = True

    # 设置请求头 - Content-Length
    if isinstance(body, str):
        body = body.encode(flymefce.DEFAULT_ENCODING)
    if not body:
        headers[http_headers.CONTENT_LENGTH] = 0
    elif isinstance(body, bytes):
        headers[http_headers.CONTENT_LENGTH] = len(body)
    elif http_headers.CONTENT_LENGTH not in headers:
        raise ValueError(b'No %s is specified.' % http_headers.CONTENT_LENGTH)

    # store the offset of fp body
    offset = None
    if hasattr(body, "tell") and hasattr(body, "seek"):
        offset = body.tell()

    protocol, host, port = utils.parse_host_port(request_endpoint, config.protocol)

    headers[http_headers.HOST] = host
    if port != config.protocol.default_port:
        headers[http_headers.HOST] += b':' + compat.convert_to_bytes(port)

    _, params = sign_function(config.credentials, http_method, path, headers, params)

    encoded_params = utils.get_canonical_querystring(params, False)
    if len(encoded_params) > 0:
        uri = path + b'?' + encoded_params
    else:
        uri = path

    # 设置请求头 Content-Type
    if http_headers.CONTENT_TYPE not in headers:
        headers[http_headers.CONTENT_TYPE] = http_content_types.TEXT_PLAIN

    # 设置请求头 Content-MD5
    # if http_headers.CONTENT_MD5 not in headers:
    #     headers[http_headers.CONTENT_MD5] = utils.generate_content_md5(body)

    # 设置请求头 x-ic-ak
    if http_headers.FLYME_IC_AK not in headers:
        if params.get('ak'):
            headers[http_headers.FLYME_IC_AK] = params['ak']

    # 设置请求头 x-ic-request-id
    if http_headers.FLYME_REQUEST_ID not in headers:
        headers[http_headers.FLYME_REQUEST_ID] = uuid.uuid4().hex

    check_headers(headers)

    retries_attempted = 0
    errors = []
    while True:
        conn = None
        try:
            # restore the offset of fp body when retrying
            # 设置请求头 - Date
            if should_get_new_date is True:
                headers[http_headers.DATE] = utils.get_gmt_time()
                headers[http_headers.FCE_DATE] = utils.get_canonical_time()

            if retries_attempted > 0 and offset is not None:
                body.seek(offset)

            conn = _get_connection(protocol, host, port, config.connection_timeout_in_mills)

            _logger.debug(
                'request args:method=%s, uri=%s, headers=%s, patams=%s, body=%s', http_method, uri, headers, params, body
            )

            http_response = _send_http_request(
                conn, http_method, uri, headers, body, config.send_buf_size
            )
            # content = http_response.read()
            # if content:
            #     content = json.loads(content)
            headers_list = http_response.getheaders()

            # on py3 ,values of headers_list is decoded with ios-8859-1 from
            # utf-8 binary bytes

            # headers_list[*][0] is lowercase on py2
            # headers_list[*][0] is raw value py3
            if compat.PY3 and isinstance(headers_list, list):
                temp_heads = []
                for k, v in headers_list:
                    k = k.encode('latin-1').decode('utf-8')
                    v = v.encode('latin-1').decode('utf-8')
                    k = k.lower()
                    temp_heads.append((k, v))
                headers_list = temp_heads

            _logger.debug('request return: status=%d, headers=%s' % (http_response.status, headers_list))
            response = FceResponse()
            response.set_metadata_from_headers(dict(headers_list))

            for handler_function in response_handler_functions:
                if handler_function(http_response, response):
                    break

            return response

        except Exception as e:
            if conn is not None:
                conn.close()

            # insert ">>>>" before all trace back lines and then save it
            errors.append('\n'.join('>>>>' + line for line in traceback.format_exc().splitlines()))

            if config.retry_policy.should_retry(e, retries_attempted):
                delay_in_millis = config.retry_policy.get_delay_before_next_retry_in_millis(
                    e, retries_attempted
                )
                time.sleep(delay_in_millis / 1000.0)
            else:
                raise FceHttpClientError('Unable to execute HTTP request. Retried %d times. '
                                         'All trace backs:\n%s' % (retries_attempted, '\n'.join(errors)), e)

        retries_attempted += 1
