#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

stream_name = "dis_test1"
partition_id = "shardId-0000000000"
label = 'total_put_bytes_per_partition'
start_time = 1543376051
end_time = 1543389151


def partition_monitor_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.partitionMonitor(stream_name, partition_id, label, start_time, end_time)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)

    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("Use your Stream to query partitionMonitor")
    partition_monitor_test()
