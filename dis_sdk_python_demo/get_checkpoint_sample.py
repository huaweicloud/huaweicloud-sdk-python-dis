#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test1"
app_name = "a"
partition_id = "shardId-0000000000"


def get_checkpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.getCheckpoint(streamName=stream_name, appName=app_name, partitionId=partition_id)
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
