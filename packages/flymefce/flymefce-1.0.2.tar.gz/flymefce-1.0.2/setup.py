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
The setup script to install FCE SDK for python
"""
from __future__ import absolute_import
import io
import os
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with io.open(os.path.join("flymefce", "__init__.py"), "rt") as f:
    SDK_VERSION = re.search(r"SDK_VERSION = b'(.*?)'", f.read()).group(1)


setup(
    name='flymefce',
    version=SDK_VERSION,
    install_requires=['pycryptodome>=3.8.0',
                      'future>=0.6.0',
                      'six>=1.4.0'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, <4',
    packages=['flymefce',
              'flymefce.auth',
              'flymefce.http',
              'flymefce.retry',
              'flymefce.services',
              'flymefce.services.fos',
              'flymefce.services.sts'],
    url='https://yun.flyme.com/#/product/fos/index',
    license='Apache License 2.0',
    author='qi.sun',
    author_email='qi.sun@xjmz.com',
    description='FOS SDK for python based on Flymeyun Cloud Engine',
)
