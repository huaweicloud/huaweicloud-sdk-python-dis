# Copyright 2002-2010 the original author or authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/python
# -*- coding:utf-8 -*-
'''
Created on 2018��4��21��

'''
def safe_encode(item):
    if isinstance(item, str):
        try:
            item = item.encode('UTF-8')
        except UnicodeDecodeError:
            try:
                item = item.encode('GB2312')
            except Exception:
                item = None
    return item

def toString(item):
    try:
        return str(item) if item is not None else ''
    except Exception:
        return ''
    
def validateString(item, maxlen):
    if (len(item) >= maxlen):
        return -1
    return ''