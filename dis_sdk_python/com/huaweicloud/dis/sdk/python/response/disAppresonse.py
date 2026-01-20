#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class disCreateAppResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)



class disdescribeAppResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)



class disApplistResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
        self.has_more_app=body.get('has_more_app','')
        self.apps=body.get('apps','')



class disDeleteAppResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
