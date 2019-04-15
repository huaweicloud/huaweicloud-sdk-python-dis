#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

streamname = "dis_test1"

def deleteStream_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r= cli.deleteStream(streamname)
        print(r.statusCode)
    except Exception as ex:
       print(str(ex))




if __name__ == '__main__':
    print("delete Stream")
    deleteStream_test()


