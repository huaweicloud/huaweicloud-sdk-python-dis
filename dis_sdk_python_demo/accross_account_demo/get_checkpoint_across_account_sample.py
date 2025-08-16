#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxxxx"
appName = "a"
partitionId = "shardId-0000000000"


def get_checkpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.getCheckpoint(streamName=streamName, appName=appName, partitionId=partitionId, streamId=streamId)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start get your Checkpoint")
    get_checkpoint_test()
