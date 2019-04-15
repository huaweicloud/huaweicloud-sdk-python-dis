#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class dischangepartitionCountResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)


class dischangedatatypeResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
