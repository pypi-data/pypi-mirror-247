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
This module defines exceptions for FCE.
"""

from flymefce import utils
from builtins import str
from builtins import bytes


class FceError(Exception):
    """Base Error of FCE."""
    def __init__(self, message):
        Exception.__init__(self, message)


class FceClientError(FceError):
    """Error from FCE client."""
    def __init__(self, message):
        FceError.__init__(self, message)


class FceServerError(FceError):
    """Error from FCE servers."""
    REQUEST_EXPIRED = b'RequestExpired'

    """Error threw when connect to server."""
    def __init__(self, message, status_code=None, code=None, request_id=None):
        FceError.__init__(self, message)
        self.status_code = status_code
        self.code = code
        self.request_id = request_id


class FceHttpClientError(FceError):
    """Exception threw after retry"""
    def __init__(self, message, last_error):
        FceError.__init__(self, message)
        self.last_error = last_error
