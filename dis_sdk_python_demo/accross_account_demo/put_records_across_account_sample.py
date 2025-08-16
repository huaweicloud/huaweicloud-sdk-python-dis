#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamId = "xxxxxxx"

def put_records_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')

    records = []
    record1 = {"data": '{"a":"xx1"}', "partition_id": 'shardId-0000000000'}
    record2 = {"data": '{"a":"xxx4445"}', "partition_id": 'shardId-0000000000'}
    records.append(record1)
    records.append(record2)

    try:
        r = cli.put_records("", streamId, records)
        print(r.statusCode)
        try:
            print(json.dumps(r.body))
        except:
            print(r.body)

    except Exception as ex:
        print(str(ex))

if __name__ == '__main__':
    print("Use your Stream to putRecords")
    put_records_test()
