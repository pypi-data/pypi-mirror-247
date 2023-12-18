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
This module provides general http handler functions for processing http responses from FCE services.
"""

import http.client
from builtins import str
from builtins import bytes
import json
from flymefce import utils
from flymefce import compat
from flymefce.exception import FceClientError
from flymefce.exception import FceServerError


def parse_json(http_response, response):
    """If the body is not empty, convert it to a python object and set as the value of
    response.body. http_response is always closed if no error occurs.

    :param http_response: the http_response object returned by HTTPConnection.getresponse()
    :type http_response: httplib.HTTPResponse

    :param response: general response object which will be returned to the caller
    :type response: flymefce.FceResponse

    :return: always true
    :rtype bool
    """
    body = http_response.read()
    if body:
        body = compat.convert_to_string(body)
        response.__dict__.update(json.loads(body, object_hook=utils.dict_to_python_object).__dict__)
        response.__dict__["raw_data"] = body
    http_response.close()
    return True


def parse_error(http_response, response):
    """If the body is not empty, convert it to a python object and set as the value of
    response.body. http_response is always closed if no error occurs.

    :param http_response: the http_response object returned by HTTPConnection.getresponse()
    :type http_response: httplib.HTTPResponse

    :param response: general response object which will be returned to the caller
    :type response: flymefce.FceResponse

    :return: false if http status code is 2xx, raise an error otherwise
    :rtype bool

    :raise flymefce.exception.FceClientError: if http status code is NOT 2xx
    """
    if http_response.status // 100 == http.client.OK // 100:
        return False

    if http_response.status // 100 == http.client.CONTINUE // 100:
        raise FceClientError(b'Can not handle 1xx http status code')

    bse = None
    body = http_response.read()
    if body:
        d = json.loads(compat.convert_to_string(body))
        bse = FceServerError(d.get('message', d.get('msg', d.get('error_msg'))),
                             code=d.get('code'),
                             request_id=d.get('requestId'))
    if bse is None:
        bse = FceServerError(http_response.reason, request_id=response.metadata.ic_request_id)
    bse.status_code = http_response.status

    raise bse
