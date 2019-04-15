#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
appName="a"

def deleteCheckpoint_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.deleteCheckpoint(streamName=streamname,appName=appName)
        print(r.statusCode)
    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("start commit your Checkpoint")
    deleteCheckpoint_test()

