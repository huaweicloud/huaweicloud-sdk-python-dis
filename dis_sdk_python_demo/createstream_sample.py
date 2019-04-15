#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name="dis_test1"
partition_count=1


def createStream_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.createStream(stream_name,partition_count,data_type='JSON',stream_type='COMMON')
        print(r.statusCode)

    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("start createStream ")
    createStream_test()
