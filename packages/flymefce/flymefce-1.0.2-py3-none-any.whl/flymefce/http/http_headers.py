# Copyright 2014 Flyme, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License") you may not use this file
# except in compliance with the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the
# License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions
# and limitations under the License.

"""
This module defines string constants for HTTP headers
"""

# Standard HTTP Headers

AUTHORIZATION = b"Authorization"

CACHE_CONTROL = b"Cache-Control"

CONTENT_DISPOSITION = b"Content-Disposition"

CONTENT_ENCODING = b"Content-Encoding"

CONTENT_LENGTH = b"Content-Length"

CONTENT_MD5 = b"Content-MD5"

CONTENT_RANGE = b"Content-Range"

CONTENT_TYPE = b"Content-Type"

DATE = b"Date"

ETAG = b"ETag"

EXPIRES = b"Expires"

HOST = b"Host"

LAST_MODIFIED = b"Last-Modified"

RANGE = b"Range"

SERVER = b"Server"

USER_AGENT = b"User-Agent"

# FCE Common HTTP Headers

FCE_PREFIX = b"x-ic-"

FCE_ACL = b"x-ic-acl"

FCE_CONTENT_SHA256 = b"x-ic-content-sha256"

FCE_COPY_METADATA_DIRECTIVE = b"x-ic-metadata-directive"

FCE_COPY_SOURCE = b"x-ic-copy-source"

FCE_COPY_SOURCE_IF_MATCH = b"x-ic-copy-source-if-match"

FCE_COPY_SOURCE_IF_MODIFIED_SINCE = b"x-ic-copy-source-if-modified-since"

FCE_COPY_SOURCE_IF_NONE_MATCH = b"x-ic-copy-source-if-none-match"

FCE_COPY_SOURCE_IF_UNMODIFIED_SINCE = b"x-ic-copy-source-if-unmodified-since"

FCE_COPY_SOURCE_RANGE = b"x-ic-copy-source-range"

FCE_DATE = b"x-ic-date"

FCE_USER_METADATA_PREFIX = b"x-ic-meta-"

FCE_REQUEST_ID = b"x-ic-request-id"

# BOS HTTP Headers

FOS_DEBUG_ID = b"x-ic-fos-debug-id"

FOS_STORAGE_CLASS = b"x-ic-storage-class"

FOS_GRANT_READ = b'x-ic-grant-read'

FOS_GRANT_FULL_CONTROL = b'x-ic-grant-full-control'

FOS_FETCH_SOURCE = b"x-ic-fetch-source"

FOS_FETCH_MODE = b"x-ic-fetch-mode"

FOS_SERVER_SIDE_ENCRYPTION = b"x-ic-server-side-encryption"

FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY = b"x-ic-server-side-encryption-customer-key"

FOS_SERVER_SIDE_ENCRYPTION_CUSTOMER_KEY_MD5 = b"x-ic-server-side-encryption-customer-key-md5"

FOS_RESTORE_TIER = b"x-ic-restore-tier"

FOS_RESTORE_DAYS = b"x-ic-restore-days"

FOS_SYMLINK_TARGET = b"x-ic-symlink-target"

FOS_SYMLINK_BUCKET = b"x-ic-symlink-bucket"

FOS_FORBID_OVERWRITE = b"x-ic-forbid-overwrite"

FOS_TRAFFIC_LIMIT = b"x-ic-traffic-limit"

# STS HTTP Headers

STS_SECURITY_TOKEN = b"x-ic-security-token"

# FlymeYun HTTP Headers

# FLYME_STS_SECURITY_TOKEN 代替 STS_SECURITY_TOKEN
FLYME_STS_SECURITY_TOKEN = b'x-ic-sts-token'

FLYME_IC_AK = b'x-ic-ak'

FLYME_REQUEST_ID = b'x-ic-request-id'
