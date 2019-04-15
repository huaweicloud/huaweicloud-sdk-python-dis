#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class disCreateStreamResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)

class disCreateStreamResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)

class disDeleteResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)



class disListStreamResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.total_number = body.get("total_number",'')
        self.stream_names = body.get("stream_names",'')
        self.stream_info_list =body.get("stream_info_list",'')

    def _printResponse(self):
        print("ListStreamResponse")
        print("total_number: %d" % (self.total_number))
        print("stream_names: %s" % (self.stream_names))
        print("stream_info_list: %s" % (self.stream_info_list))




class disDescribeStreamResponse(DisResponse):

    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.streamName = body.get("stream_name","")
        self.createTime = body.get("create_time","")
        self.lastModifiedTime = body.get("last_modified_time","")
        self.retentionPeriod = body.get("retention_period","")
        self.status = body.get("status","")
        self.streamType =  body.get("stream_type","")
        self.partitions = body.get("partitions","")
        self.currentPartitionCount = len(self.partitions)
        self.hasMorePartitions = body.get("has_more_partitions","")


    def _printResponse(self):
        print ("disDescribeStreamResponse")
        print ("stream_name: %s" %(self.streamName))
        print ("create_time: %s" %(self.createTime))
        print ("last_modified_time: %s" %(self.lastModifiedTime))
        print ("retention_period: %d" %(self.retentionPeriod))
        print ("status: %s" %(self.status))
        print ("stream_type: %s" %(self.streamType))
        print ("partitions: %s" %(self.partitions))
        print ("currentPartitionCount: %d" %(self.currentPartitionCount))
        print ("has_more_partitions: %s" %(self.hasMorePartitions))


class dislistdumptaskResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.tasks = body.get("tasks", "")
        self.total_number = body.get("total_number", "")



class disdescribedumptaskResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.createTime = body.get("create_time", "")
        self.last_transfer_timestamp = body.get("last_transfer_timestamp", "")
        self.taskName = body.get("task_name", "")
        self.partitions = body.get("partitions", "")
        self.streamName = body.get("stream_name", "")
        self.status = body.get("status", "")
        self.streamType = body.get("stream_type", "")
        self.currentPartitionCount = len(self.partitions)
        self.hasMorePartitions = body.get("has_more_partitions", "")

