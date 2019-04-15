#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis-oeYF"

def describeStream_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        hasMorePartitions = True
        startPartitionId = ""
        partitions = []
        while hasMorePartitions:
            r=cli.describeStream(streamname, startPartitionId)
            hasMorePartitions = r.hasMorePartitions
            startPartitionId = r.partitions[-1].get('partition_id')
            partitions.extend(r.partitions)
            if IS_PYTHON2:
                print(json.dumps(r.body))
            else:
                print(r.body)

    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("describe your Stream")
    describeStream_test()




