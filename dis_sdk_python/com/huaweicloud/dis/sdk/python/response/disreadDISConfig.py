#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class disgetDisclientResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self,statusCode,body)
        self.projectid = body['projectid']
        self.ak = body['ak']
        self.sk = body['sk']
        self.region = body['region']
        self.endpoint = body['endpoint']





