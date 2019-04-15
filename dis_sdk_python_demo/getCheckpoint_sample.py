#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
appName="a"
partitionId="shardId-0000000000"


def getCheckpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.getCheckpoint(streamName=streamname, appName=appName, partitionId=partitionId)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("start get your Checkpoint")
    getCheckpoint_test()

