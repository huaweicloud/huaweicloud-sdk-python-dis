#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"

def list_dump_task_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.list_dump_task(streamname)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)

    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print("list dump_task")
    list_dump_task_test()




