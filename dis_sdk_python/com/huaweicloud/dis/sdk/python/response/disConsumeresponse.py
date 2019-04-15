#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse


class disGetConsumeresponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
        self.stream_name = body.get("stream_name",'')
        self.partition_consuming_states=body.get("partition_consuming_states",'')
        self.app_name = body.get("app_name",'')

    def _printResponse(self):
        print("getMonitorresponse")
        print("stream_name: %s" % (self.stream_name))
        print("partition_consuming_states: %s" % (self.partition_consuming_states))
        print("app_name: %s" % (self.app_name))



