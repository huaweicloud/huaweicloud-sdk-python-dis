#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxx"
appName = "a"
partitionId = "shardId-0000000000"
seqNumber = "0"


def commit_checkpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.commitCheckpoint(streamName=streamName, streamId=streamId, appName=appName, partitionId=partitionId, seqNumber=seqNumber)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start commit your Checkpoint")
    commit_checkpoint_test()
