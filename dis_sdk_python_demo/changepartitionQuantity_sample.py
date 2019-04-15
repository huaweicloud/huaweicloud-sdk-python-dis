#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

target_partition_count=1
streamname="dis_test1"

def changepartitionQuantity_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.changepartitionQuantity(stream_name_test=streamname,target_partition_count=target_partition_count)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)
    except Exception as ex:
        print(str(ex))




if __name__ == '__main__':
    print("start change your partitionQuantity")
    changepartitionQuantity_test()

