#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test1"
partition_id = "shardId-0000000000"


def get_cursor_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        # startSeq与AT_SEQUENCE_NUMBER/AFTER_SEQUENCE_NUMBER搭配使用
        r = cli.getCursor(stream_name, partition_id, cursorType='AT_SEQUENCE_NUMBER', startSeq="0")
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to get Cursor")
    get_cursor_test()
