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
Created on 2018��4��24��
'''
import base64
from dis.disresponse import DisResponse

class disPutRecordsResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.failedRecordCount = body["failed_record_count"] 
        self.recordResult = body["records"]   

    def _printResponse(self):
        print ("PutRecordsResponse")
        print ("failed_record_count: %d" %(int(self.failedRecordCount)))
        print ("recordResult %s: " %(self.recordResult))
        
    def getSendFailuerRecord(self, originRecords):
        failRecord = [];
        if self.failed_record_count == 0:
            return failRecord
        
        for i in range(len(self.recordResult)):
            if "sequence_number" in self.recordResult[i].keys():
                pass
            else :
                failRecord.append(originRecords[i])
        
        return failRecord


class disGetCursorResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.cursor = body["partition_cursor"]
        
    def _printResponse(self):
        print ("GetCursorResponse")
        print ("cursor: %s" %(self.cursor))
        
        
class disGetRecordsResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.nextPartitionCursor = body["next_partition_cursor"] 
        self.recordResult = body["records"]  
        self.recordCount = len(body["records"]) 
        for i in range(self.recordCount):
            tempData = self.recordResult[i]["data"].encode('utf-8')
            self.recordResult[i]["data"] = str(base64.b64decode(tempData), 'utf-8')

    def _printResponse(self):
        print ("PutRecordsResponse")
        print ("next_partition_cursor: %s" %(self.nextPartitionCursor))        
        print ("recordCount %d" %(self.recordCount))
        print ("recordResult %s: " %(self.recordResult))
        
