#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamName = "dis-oeYF"
streamId = "xxxxxxx"


def describe_stream_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        has_more_partitions = True
        start_partition_id = ""
        partitions = []
        while has_more_partitions:
            r = cli.describeStream(streamName, start_partition_id, streamId=streamId)
            has_more_partitions = r.hasMorePartitions
            start_partition_id = r.partitions[-1].get('partition_id')
            partitions.extend(r.partitions)
            if IS_PYTHON2:
                print(json.dumps(r.body))
            else:
                print(r.body)

    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("describe your Stream")
    describe_stream_test()
