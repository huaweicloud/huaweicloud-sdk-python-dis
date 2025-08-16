#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxxxx"
appName = "a"



def delete_checkpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.deleteCheckpoint(streamName=streamName, streamId=streamId, appName=appName)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start commit your Checkpoint")
    delete_checkpoint_test()
