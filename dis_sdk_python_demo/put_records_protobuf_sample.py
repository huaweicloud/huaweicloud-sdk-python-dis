#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test"
# stream_name = ""
stream_id = "xxxxxxxxxxxxxxxxxxx"


def put_records_protobuf_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='', bodySerializeType='protobuf')

    records = []
    record1 = {"data": "xxxxx", "partition_key": '0'}
    record2 = {"data": "xxxxx", "partition_key": '0'}
    records.append(record1)
    records.append(record2)

    try:
        r = cli.putRecords(stream_name, records)
        print(r.statusCode)
        try:
            print(json.dumps(r.body))
        except:
            print(r.body)

    except Exception as ex:
        print(ex)


def put_records_protobuf_test_stream_id():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='', bodySerializeType='protobuf')

    records = []
    record1 = {"data": "xxxxx", "partition_key": '0'}
    record2 = {"data": "xxxxx", "partition_key": '0'}
    records.append(record1)
    records.append(record2)

    try:
        r = cli.put_records(stream_name, stream_id, records)
        print(r.statusCode)
        try:
            print(json.dumps(r.body))
        except:
            print(r.body)
    except Exception as ex:
        print(ex)

if __name__ == '__main__':
    print("Use your Stream to put records using protobuf")
    put_records_protobuf_test()
    put_records_protobuf_test_stream_id()
