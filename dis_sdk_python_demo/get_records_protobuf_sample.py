#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test1"
partitionId = "shardId-0000000000"


def get_records_protobuf_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='', bodySerializeType='protobuf')
    try:
        r = cli.getCursor(stream_name, partitionId, cursorType='AT_SEQUENCE_NUMBER', startSeq="0")

        cursor = r.cursor
        while cursor:
            r = cli.getRecords(partitioncursor=cursor)
            cursor = r.nextPartitionCursor
            if r.recordResult:
                print(r.statusCode)
                # print(r.recordResult)
                try:
                    print(json.dumps(r.body))
                except:
                    print(r.body)

            else:break
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to get records using protobuf")
    get_records_protobuf_test()


