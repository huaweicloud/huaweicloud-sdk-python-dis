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
Created on 2018��4��19��

'''
import ssl
import requests
import urllib3
from dis import disauth


requests.packages.urllib3.disable_warnings()
class disRequest(object):
    def __init__(self, method, host, uri, protocol="https", query={}, headers={}, body=""):
        self.method = method
        self.protocol = protocol  # http/https
        self.host = host  # example.com
        self.uri = uri  # /request/uri
        self.query = query
        self.headers = headers
        self.body = body


    def _getResponse(self, method, uri, timeout, params={}, headers={}, body=""):
        try:
            r = requests.request(method, uri, params=params, data=body, headers=headers, timeout=timeout, verify=False)
            return r.status_code, r.content, r.headers
        except Exception as ex:
            raise print('_getResponse', str(ex)) 


    def _sendRequest(self, method, uri, timeout, params={}, headers={}, body=""):
        pass
    '''
    def getresponse(self, ssl_verify=False):
        if self.protocol.lower() == 'http':
            req = HTTPConnection(self.host, port=self.port)
        else:
            if ssl_verify:
                req = HTTPSConnection(self.host, port=self.port)
            else:
                req = HTTPSConnection(self.host, port=self.port, context=ssl._create_unverified_context())
        req.connect()
        req.putrequest(self.method, self.uri)

        for key in self.headers:
            req.putheader(key, self.headers[key])
        req.endheaders(self.body.encode('utf-8'))
        req.request(self.method, self.uri, self.body)
        r=requests.request("GET" ,url, headers=req.headers, params=req.query, data=req.body,verify=False)
        '''
