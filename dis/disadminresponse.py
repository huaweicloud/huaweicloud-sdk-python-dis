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

from dis.disresponse import DisResponse

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
            