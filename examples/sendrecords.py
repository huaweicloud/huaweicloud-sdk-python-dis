#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis import disclient
from dis import disresponse
from dis import disrecordresponse

def test():
    cli = disclient.disclient("endpoint",'ak', 'sk','projectid', 'region')
    
    
   
    streamName = "test_py"
    try:
        
        records = []
        record1 = {"data":"abcdefgxxxxxxx", "partition_key":"1"}
        record2 = {"data":"hijklmnllllllllll", "partition_key":"2"}
        record3 = {"data":"opqrsteeeeeee", "partition_key":"3"}
        record4 = {"data":"uvwxyzjhwfuehfua", "partition_key":"4"}
        record5 = {"data":"okjfurjfajff", "partition_key":"5"}
        
        records.append(record1)
        records.append(record2)   
        records.append(record3)
        records.append(record4)
        records.append(record5)  
        
           
        r = cli.putRecords(streamName, records)
        r._printResponse()
        
        if r.failedRecordCount is not 0:
            recordsFailure = r.getSendFailuerRecord(records)   
            r = cli.putRecords(streamName, recordsFailure)
            
        r = cli.describeStream(streamName)
        r._printResponse()
            
            
    except Exception as ex:
        print (str(ex))
    


if __name__ == '__main__':
    print("hello world")
    test()