#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
appName="a"
partitionId="shardId-0000000000"
seqNumber="0"


def commitCheckpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.commitCheckpoint(streamName=streamname,appName=appName,partitionId=partitionId,seqNumber=seqNumber)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("start commit your Checkpoint")
    commitCheckpoint_test()

