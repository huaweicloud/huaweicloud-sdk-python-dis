#!/usr/bin/python
# -*- coding:utf-8 -*-
from dis_sdk_python import *

start_stream_name = ""

def listStream_test():
    cli = disclient(endpoint='', ak='', sk='', projectid='', region='')
    try:
        r=cli.listStream(start_stream_name)
        print(r.statusCode)
        if IS_PYTHON2:
            print(json.dumps(r.body))
        else:
            print(r.body)

    except Exception as ex:
        print(str(ex))



if __name__ == '__main__':
    print('list your Stream')
    listStream_test()

