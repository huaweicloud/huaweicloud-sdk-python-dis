#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

target_partition_count = 1
stream_name = "dis_test1"


def change_partition_quantity_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r = cli.changepartitionQuantity(stream_name_test=stream_name, target_partition_count=target_partition_count)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))


if __name__ == '__main__':
    print("start change your partitionQuantity")
    change_partition_quantity_test()
