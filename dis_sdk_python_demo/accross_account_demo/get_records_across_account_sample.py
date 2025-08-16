#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis_test1"
streamId = "xxxxxxx"
partitionId = "shardId-0000000000"


def getRecords_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.getCursor(streamName, partitionId, cursorType='AT_SEQUENCE_NUMBER', startSeq="0", streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='AFTER_SEQUENCE_NUMBER', startSeq="0", streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='AFTER_SEQUENCE_NUMBER', startSeq="0", streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='AT_TIMESTAMP',timestamp=1554694135190, streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='TRIM_HORIZON', streamId=streamId)
        # r = cli.getCursor(streamName, partitionId, cursorType='LATEST', streamId=streamId)
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
                # for i in r.getRecordResult(r.recordResult):
                #     print("record[{}],sequenceNumber[{}],partitionKey[{}],timestamp[{}],timestamp_type[{}]".format(
                #         i.data, i.sequence_number, i.partitionKey,i.timestamp,i.timestamp_type))
            else:
                break

    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to get data")
    getRecords_test()
