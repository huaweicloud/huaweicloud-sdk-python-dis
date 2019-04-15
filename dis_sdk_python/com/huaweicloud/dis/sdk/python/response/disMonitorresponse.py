#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class disGetMonitorResponse(DisResponse):
    def __init__(self, status_code, body):
        DisResponse.__init__(self, status_code, body)
        self.metrics = body.get("metrics")
        self.label=self.metrics.get('label')
        self.dataPoints = self.metrics.get('dataPoints')


    def _printResponse(self):
        print("getMonitorresponse")
        print("metrics: %s" % (self.metrics))
        print("label: %s" % (self.label))
        print("dataPoints: %s" % (self.dataPoints))
