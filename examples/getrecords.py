#!/usr/bin/python
# -*- coding:utf-8 -*-

from dis import disclient
from dis import disresponse
from dis import disrecordresponse

def test():
    #cli = disclient.disclient("endpoint",'ak', 'sk','projectid', 'region')
    cli = disclient.disclient("dis.cn-north-1.myhuaweicloud.com:20004",'ODO387IHGUPDQRH2BH6Z', '2xDa0FHfrzDKEooKogZrcghmdqBiWii5XjLCe3Ce','c159a24641da49b2a729ea6f57647888', 'cn-north-1')
    
    
    
    streamName = "test_py"
    
    try:
        r = cli.describeStream(streamName)
        
        if r.statusCode is 200:
            
            for partition in r.partitions :
                
                r1 = cli.getCursor(streamName, partition["partition_id"], "TRIM_HORIZON", '', ak = "12345456666635", sk = "asdfjhjrgadhjkadfahsdifhaejf")
                
                if r1.statusCode is 200:

                    r2 = cli.getRecords(r1.cursor, 0)
                    if r2.statusCode is 200:
                        print ("partitionid: %s" %(partition["partition_id"]))
                        print (r2.recordCount)
                        print (r2.nextPartitionCursor)
                        print (r2.recordResult)

    except Exception as ex:
        print (str(ex))    
        
        
if __name__ == '__main__':
    print("get records test")
    test()
                