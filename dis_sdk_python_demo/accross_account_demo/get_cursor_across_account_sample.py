#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxxxx"
partitionId = "shardId-0000000000"


def get_cursor_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        # startSeq与AT_SEQUENCE_NUMBER/AFTER_SEQUENCE_NUMBER搭配使用
        r = cli.getCursor(streamName, partitionId, cursorType='AT_SEQUENCE_NUMBER', startSeq="0", streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='AFTER_SEQUENCE_NUMBER', startSeq="0", streamId=streamId)
        # timestamp与AT_TIMESTAMP搭配使用
        # r = cli.getCursor(streamName, partitionId, cursorType='AT_TIMESTAMP',timestamp=1554694135190, streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='TRIM_HORIZON', streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='LATEST', streamId=streamId)
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
