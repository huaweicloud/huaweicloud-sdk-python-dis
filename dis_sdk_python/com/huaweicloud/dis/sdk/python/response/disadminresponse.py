#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse

class disCreateStreamResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        
class disDeleteStreamResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        
class disListStreamResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.total = body["total_number"]
        self.streams = body["stream_names"]
        self.count = len(self.streams)
        self.hasMoreStream = body["has_more_streams"]

        
    def _printResponse(self):
        print ("ListStreamResponse")
        print ("total stream: %d" %(self.total))
        print ("has more streams: %s" %(self.hasMoreStream))
        print ("streams: %s" %(self.streams))
        print ("current count: %d" %(self.count))

class disDescribeStreamResponse(DisResponse):

    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.streamName = body["stream_name"]
        self.createTime = body["create_time"]
        self.lastModifiedTime = body["last_modified_time"]
        self.retentionPeriod = body["retention_period"]
        self.status = body["status"]
        self.streamType = body["stream_type"]
        self.partitions = body["partitions"]
        self.currentPartitionCount = len(self.partitions)
        self.hasMorePartitions = body["has_more_partitions"]



    def _printResponse(self):
        print ("DescribeStreamResponse")
        print ("stream_name: %s" %(self.streamName))
        print ("create_time: %s" %(self.createTime))
        print ("last_modified_time: %s" %(self.lastModifiedTime))
        print ("retention_period: %d" %(self.retentionPeriod))
        print ("status: %s" %(self.status))
        print ("stream_type: %s" %(self.streamType))
        print ("partitions: %s" %(self.partitions))
        print ("currentPartitionCount: %d" %(self.currentPartitionCount))
        print ("has_more_partitions: %s" %(self.hasMorePartitions))

class disDescribeStreamresultResponse(disDescribeStreamResponse):

    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.partitions = body['partitions']
        self.streamName = body["stream_name"]
        self.createTime = body["create_time"]
        self.lastModifiedTime = body["last_modified_time"]
        self.retentionPeriod = body["retention_period"]
        self.status = body["status"]
        self.streamType = body["stream_type"]
        self.partitions = body["partitions"]
        self.currentPartitionCount = len(self.partitions)
        self.hasMorePartitions = body["has_more_partitions"]
        for i in self.partitions:
            self.hash_range = i.get('hash_range')
            self.sequence_number_range =i.get('sequence_number_range')
            self.partition_id = i.get('partition_id')




    def _printResponse(self):
        print ("DescribeStreamResponse")
        print ("stream_name: %s" %(self.streamName))
        print ("create_time: %s" %(self.createTime))
        print ("last_modified_time: %s" %(self.lastModifiedTime))
        print ("retention_period: %d" %(self.retentionPeriod))
        print ("status: %s" %(self.status))
        print ("stream_type: %s" %(self.streamType))
        print ("partitions: %s" %(self.partitions))
        print ("currentPartitionCount: %d" %(self.currentPartitionCount))
        print ("has_more_partitions: %s" %(self.hasMorePartitions))
        print ("hash_range: %s" % (self.hash_range))
        print ("sequence_number_range: %s" % (self.sequence_number_range))
        print ("partition_id: %s" % (self.partition_id))



class dislistdumptaskResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.has_more_tasks = body['has_more_tasks']
        self.total_number = body['total_number']
        self.details = body['details']

    def _printResponse(self):
        print("dislistdumptaskResponse")
        print('has_more_tasks:%s' % (self.has_more_tasks))
        print('total_number:%s' % (self.total_number))
        print('details:%s' % (self.details))


class disdescribedumptaskResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.body = body

