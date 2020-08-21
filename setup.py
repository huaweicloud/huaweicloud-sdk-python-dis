# !/usr/bin/env python
# -*- coding:utf-8 -*-
# Copyright 2019 Huawei Technologies Co.,Ltd.
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License.  You may obtain a copy of the
# License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations under the License.

# use 'python setup.py bdist_egg' to generate the egg file package
# use 'easy_install eggfile' to install the egg file to the python Lib

# or

# use 'python setup.py install' to install to the python Lib directly

from setuptools import setup, find_packages
setup(
    name='huaweicloud-python-sdk-dis',
    version='2.0.4',
    description='Huawei Cloud DIS SDK for Python',
    url='https://github.com/huaweicloud/huaweicloud-sdk-python-dis',
    author='Huawei',
    author_email='',
    license='Apache-2.0',
    classifiers=[
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages=find_packages(),
    zip_safe=False,
    keywords=('dis', 'python'),
    install_requires=[
        'requests',
        'chardet',
        'urllib3',
        'protobuf'
    ],
    package_data={'dis_sdk_python': ['*.txt', '*.conf']}
)

