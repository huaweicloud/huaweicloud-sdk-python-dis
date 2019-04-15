#!/usr/bin/python
#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
partitionId="shardId-0000000000"


def getCursor_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        # startSeq与AT_SEQUENCE_NUMBER/AFTER_SEQUENCE_NUMBER搭配使用
        r = cli.getCursor(streamname, partitionId, cursorType='AT_SEQUENCE_NUMBER', startSeq="0")
        # r = cli.getCursor(streamname, partitionId, cursorType='AFTER_SEQUENCE_NUMBER', startSeq="0")
        # timestamp与AT_TIMESTAMP搭配使用
        # r = cli.getCursor(streamname, partitionId, cursorType='AT_TIMESTAMP',timestamp=1554694135190)
        # r = cli.getCursor(streamname, partitionId, cursorType='TRIM_HORIZON')
        # r = cli.getCursor(streamname, partitionId, cursorType='LATEST')
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("Use your Stream to get Cursor")
    getCursor_test()

