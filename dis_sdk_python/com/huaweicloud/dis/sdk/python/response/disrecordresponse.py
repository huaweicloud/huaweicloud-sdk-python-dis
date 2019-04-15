#!/usr/bin/python
# -*- coding:utf-8 -*-

import base64
from dis_sdk_python.com.huaweicloud.dis.sdk.python.response.disresponse import DisResponse


class disPutRecordsResponse(DisResponse):
    
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        if body and type(body) != dict:
            from dis_sdk_python.com.huaweicloud.dis.sdk.python.proto import record_pb2
            target = record_pb2.PutRecordsResult()
            target.ParseFromString(body)
            records=[]
            self.body = {}
            records.extend([{'partition_id': target.records[i].shardId,
                             'sequence_number':target.records[i].sequenceNumber,
                             'error_message':target.records[i].errorMessage,
                             'error_code': target.records[i].errorCode} for i in
                            range(len(target.records))])

            for i in records:
                if 'DIS' not in i['error_code']:
                    del i['error_code']
                    del i['error_message']

            self.body['records'] = records
            self.body['failed_record_count']=target.failedRecordCount
        else:
            self.body = body

        self.failedRecordCount = self.body["failed_record_count"]
        self.recordResult = self.body["records"]


    def _printResponse(self):
        print ("PutRecordsResponse")
        print ("failed_record_count: %d" %(int(self.failedRecordCount)))
        print ("recordResult %s: " %(self.recordResult))


    def getSendFailuerRecord(self, originRecords):
        failRecord = []

        if self.failedRecordCount == 0:
            return failRecord

        for i in range(len(self.recordResult)):
            if "sequence_number" in self.recordResult[i].keys():
                pass

            else :
                failRecord.append(originRecords[i])

        return failRecord

    def getSendRecordResult(self,originRecords):
        r=ListObj(originRecords)
        return r


class ListObj(object):
    def __init__(self, a):
        self.count = -1
        self.a = a

    def __iter__(self):
        return self

    def next(self):
        self.count += 1
        if self.count >= len(self.a):
            raise StopIteration()
        return self

    def __next__(self):
        self.count += 1
        if self.count >= len(self.a):
            raise StopIteration()
        return self

    def setValue(self, name, value):
        setattr(self, name, value)

    def __getattr__(self, key):
        return self.a[self.count].get(key,'')


class disPutFileRecordsResponse(DisResponse):
    def __init__(self, statusCode, body):
        DisResponse.__init__(self, statusCode, body)
        self.recordResult=[]
        self.failedRecordCount=0
        for i in body:
            self.failedRecordCount+=i['failed_record_count']
            self.recordResult.extend(i['records'])
        self.body={'failed_record_count':self.failedRecordCount,
                   'records':self.recordResult
                   }

    def getSendFailuerRecord(self, originRecords):
        failRecord = []

        if self.failedRecordCount == 0:
            return failRecord

        for i in range(len(self.recordResult)):
            if "sequence_number" in self.recordResult[i].keys():
                pass

            else :
                failRecord.append(originRecords[i])

        return failRecord

    def getSendRecordResult(self,originRecords):
        r=ListObj(originRecords)
        return r

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
        self.body = {}
        if type(body)==dict:
            self.body['next_partition_cursor'] = body["next_partition_cursor"]
            for i in range(len(body["records"])):
                tempData = body["records"][i]["data"].encode('utf-8')
                try:
                    body["records"][i]["data"] = base64.b64decode(tempData).decode('utf-8')
                except:
                    body["records"][i]["data"] = base64.b64decode(tempData)
            self.body['records'] = [{'data': i.get('data'),
                                     'sequence_number': i.get('sequence_number'),
                                     'partitionKey':i.get('partition_key'),
                                     'timestamp':i.get('timestamp'),
                                     'timestamp_type':i.get('timestamp_type')
                                     } for i in body["records"]]

        else:
            from dis_sdk_python.com.huaweicloud.dis.sdk.python.proto import record_pb2
            target= record_pb2.GetRecordsResult()
            target.ParseFromString(body)
            records=[{'sequence_number':i.sequenceNumber,
                      'data':i.data,
                      'partitionKey':i.partitionKey,
                      'timestamp':i.timestamp,
                      'timestamp_type':i.timestampType
                      } for i in list(target.records)]
            for i in records:
                if not i['partitionKey']:i['partitionKey'] = None
            self.body['next_partition_cursor']=target.nextShardIterator
            self.body['records']=records


        self.nextPartitionCursor = self.body["next_partition_cursor"]
        self.recordResult = self.body["records"]
        self.recordCount = len(self.body["records"])

    def _printResponse(self):
        print ("GetRecordsResponse")
        print ("next_partition_cursor: %s" %(self.nextPartitionCursor))
        print ("recordCount %d" %(self.recordCount))
        print ("recordResult %s: " %(self.recordResult))
        
    def getRecordResult(self,originRecords):
        r=ListObj(originRecords)
        return r


