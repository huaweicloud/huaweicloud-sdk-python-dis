#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
from dis_sdk_python.com.huaweicloud.dis.sdk.python.models.disexception import DisException

# requests.packages.urllib3.disable_warnings()
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
            raise DisException('_getResponse', str(ex))



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
