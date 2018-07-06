#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis import disclient
from dis import disadminresponse
from dis import disrecordresponse
import base64
from time import sleep

def test():
    
    cli = disclient.disclient("endpoint",'ak', 'sk','projectid', 'region')
    
    
    
    streamname = "test_py"
    
    #sleep(2)
    try:
        records = []
        record1 = {"data":"abcdefg", "partition_key":"1"}
        record2 = {"data":"hijklmn", "partition_key":"2"}
        
        records.append(record1)
        records.append(record2)
        
        print (records)
        '''
        r1 = cli.createStream(streamname, 2)
        print (r1.status_code)
        print (r1.body)    
        '''
        r3 = cli.describeStream(streamname)
        partitionId = r3.partitions[1]['partition_id']
        print (partitionId)
        print (type(partitionId))
        
        
        
        r2 = cli.putRecords(streamname, records)
        print (r2.statusCode)
        print (r2.failedRecordCount)
        
        
        r4 = cli.getCursor(streamname, partitionId, 'TRIM_HORIZON', '0')
        print (r4.statusCode)
        print (r4.cursor)
        print (type(r4.cursor))
        
        r5 = cli.getRecords(r4.cursor)
        r5._printResponse()
    
    except Exception as ex:
        print (str(ex))


if __name__ == '__main__':
    print("hello world")
    test()