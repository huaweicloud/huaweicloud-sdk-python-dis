#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"
task_name="113"

def delete_dump_task_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r= cli.delete_dump_task(streamname, task_name)
        print(r.statusCode)
    except Exception as ex:
       print(str(ex))




if __name__ == '__main__':
    print('delete dump_task')
    delete_dump_task_test()


